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
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier

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
    """Constructs and returns a model pipeline.
    """

    model = Pipeline([
        ("tfidf_vectorize", TfidfVectorizer(tokenizer=tokenize, min_df=0.001,
                                            max_features=5000)),
        ("classify", MultiOutputClassifier(DecisionTreeClassifier(**params)))
    ])

    return model

def tune_model(X, Y):
    """Runs a grid search over the model, identifying ideal parameters
    """
    params = {
        'classify__estimator__max_depth': [3, 4, 5],
        'classify__estimator__criterion': ["entropy"],
        'classify__estimator__min_samples_split': [2, 5, 10],
        'classify__estimator__max_features': ["sqrt"]
    }

    # Test model
    model = build_model()

    # Gridsearch
    gs = GridSearchCV(estimator=model, param_grid=params, verbose=2)
    
    gs.fit(X, Y)

    best_params = {
        'max_depth': gs.best_params_["classify__estimator__max_depth"],
        'criterion': "gini",
        'max_features': "sqrt",
        'min_samples_split': gs.best_params_["classify__estimator__min_samples_split"]
    }

    return best_params

def evaluate_model(model, X_test, Y_test, category_names):
    """Evaluate the multi-label model's predictions against the true values.
    """

    # Get the predictions
    Y_pred = model.predict(X_test)

    print(Y_pred)

    # For each prediction, output the classification report
    for i in range(36):
        print(f"Category: {category_names[i]}")
        print(classification_report(Y_test.iloc[:, i], Y_pred[:, i]))

def save_model(model, model_filepath):
    """Pickle a model to a file."""
    dump(model, open(model_filepath, "wb"))


def main(): 
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2,
                                                            random_state=451)

        print('Finding optimal parameters')
        params = tune_model(X_train, Y_train)

        print('Optimal parameters found')
        print(params)

        print('Building model...')
        model = build_model(params)
        
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