# Disaster Response project

## Motivation

Build a web app that allows disaster response teams to quickly identify messages on social media as disaster-related and direct the appropriate team to help.

This project forms part of the Udacity Data Scientist Nanodegree.

## Project files

The project consists of three sections:

- a data folder, containing raw data files and the script to convert them into aSQLite table

- a models folder, containing the script to create new classifiers and any stored models

- an app folder, containing the files necessary to build and run a webapp

## Instructions

## ETL pipeline

Run the following command to start the ML pipeline:

```
python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db
```

This will create and populate the SQLite database

## ML pipeline

Run the following command to start the ML pipeline:

```
python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db
```

Note that the ETL pipeline needs to have been run at least once previously for this to work.

## Web app

Run the following command to start the webapp locally:

```
python app/run.py
```

The webapp will be found at `http://localhost:3001`

Note that the database needs to have been constructed (using the ETL pipeline) and the model needs to have been created (using the ML pipeline) before the app will run successfully.