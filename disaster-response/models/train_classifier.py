import sys
import pandas as pd
from sqlalchemy import create_engine
from pickle import dump
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from nltk.tokenize import word_tokenize
from collections import defaultdict 
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support


def load_data(database_filepath):
    """Load data from SQLite into memory.
    """

    engine = create_engine(f'sqlite:///{database_filepath}')
    df = pd.read_sql_table("Messages", engine)
    X = df["message"]
    Y = df.drop(["message", "id", "original", "genre"], axis=1)

    return X, Y, Y.columns
    
def tokenize(text):
    """Converts text to tokens. Case-folds, removes stop words, lemmatises text.
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

def build_model(params={}):
    """Constructs and returns and model pipeline.
    """

    model = Pipeline([
        ("tfidf_vectorize", TfidfVectorizer(tokenizer=tokenize)),
        ("classify", MultiOutputClassifier(RandomForestClassifier(params)))
    ])

    return model


def evaluate_model(model, X_test, Y_test, category_names):
    pass


def save_model(model, model_filepath):
    """Pickle a model to a file."""
    dump(model, open(model_filepath, "wb"))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()