import json
import plotly
import pandas as pd

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from collections import defaultdict

from flask import Flask
from flask import render_template, request, jsonify
from plotly.graph_objs import Bar, Pie
from sklearn.externals import joblib
from sqlalchemy import create_engine
import sys

app = Flask(__name__)

def tokenize(text):
    """Converts text to tokens. Case-folds, removes stop words, lemmatises text.
    This is the same tokenization as is done on the training data for the model.
    """

    # Set up dict for lemmatisation
    tag_map = defaultdict(lambda : "n")  # by default, assume nouns
    tag_map['J'] = "a"  # adjectives
    tag_map['V'] = "v"  # verbs
    tag_map['R'] = "r"  # adverbs

    # Get stopword list
    stops = stopwords.words("english")

    # Create lemmatizer object
    lemma = WordNetLemmatizer()

    # Case fold
    tokens = word_tokenize(text.lower())

    # Tag tokens with parts of speech
    tokens = [(token[0], tag_map[token[1][0]]) for token in pos_tag(tokens)]

    # Lemmatise text
    tokens = [lemma.lemmatize(word=w[0], pos=w[1]) for w in tokens]

    # Remove stop & short words
    tokens = [w for w in tokens if w not in stops and len(w) > 2]

    # Return tokens
    return tokens


# load data
engine = create_engine('sqlite:///data/DisasterResponse.db')
df = pd.read_sql_table('Messages', engine)

# load model
model = joblib.load("models/classifier.pkl")


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    
    # extract data needed for visuals
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)

    # Pie chart of related values
    related_df = df["related"].value_counts()

    # create visuals
    # TODO: Below is an example - modify to create your own visuals
    graphs = [
        {
            'data': [
                Bar(
                    x=genre_names,
                    y=genre_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Message Genres',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Genre"
                }
            }
        },
        {
            'data': [
                Pie(
                    values=related_df,
                    labels=related_df.index
                )
            ],

            'layout': {
                'title': 'Pie chart of related messages count',
                
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Category", 
                    'automargin': True
                }
            }
        }
    ]
    
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '') 

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )


def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()