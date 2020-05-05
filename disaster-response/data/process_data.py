import sys
import pandas as pd
from sqlalchemy import create_engine


def load_data(messages_filepath, categories_filepath):
    """Loads and merges data from csv files. Returns a Pandas dataframe.
    """
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    
    # Merge dataframes together
    return messages.merge(categories, on="id")


def clean_data(df):
    """Cleans and processes data for storage. Returns a Pandas dataframe.
    """
    # Expand the columns
    categories = df["categories"].str.split(";", expand=True)

    # Extract colnames and overwrite originals
    categories.columns = categories.iloc[0].apply(lambda x: x[:-2])
    
    # Extract numbers from columns
    for column in categories:
        categories[column] = categories[column].apply(lambda x: x[-1]).astype(int)

    # Drop redundant column
    df.drop("categories", axis=1, inplace=True)
    
    # Combine dfs
    df = pd.concat([df, categories], axis=1)
    
    # Remove duplicate rows
    df.drop_duplicates(inplace=True)
    
    return df
        
def save_data(df, database_filename):
    """Saves a dataframe to an SQLite database.
    """
    # Save to named file
    engine = create_engine(f'sqlite:///{database_filename}')
    df.to_sql('Messages', engine, index=False)

def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()
