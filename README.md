# Rock, Paper, Scissors Game

## Overview

This is an implementation of a rock paper scissors game, developed using Python 3.10.8 and Flask. Data from the game is stored in a SQLite DB to reduce complexity and avoid hard-coding secrets (database URL, keys) in the code.

## Instructions
- Clone the repository

```bash
cd proj

# start the virtual environment
source rpsDemo/Scripts/activate

# remove existing db, if present
rm -f my-test.db

# create a new empty db
python init_db.py

# run the app; it should be available on http://127.0.0.1:5000
python -m flask run

```

## To do

Additional items I would have worked on to improve the usability and functionality of the game if I had the time.

- I would have refactored the code to make it more readable, remove repetition, and possibly used an Object Relational Model (ORM) to fecth data, rather than write SQL queries 
- I would have implemented some logging to help with debugging and monitoring
- I would have containerized the app to enable it to be deployed to a kubernetes cluster if need be
- I would have used an external database and probably experimented with a NoSQL database like MongoDB or CosmosDB
- I would have set up testing infrastructure. I started creating a set of API functions for that purpose
- I would have improved functionality for the user. Right now, data from games is being stored in the database, but the UI does not provide ways to search it or retrieve it.
- I would have improved error handling and the screening of inputs, and used Javascript to check user inputs in the GUI
- I would have devised a better way to identify and retrieve individual games, to account for simultaneous use by multiple users
- I would also have considered other API frameworks such as Django, Express or Restify
- I would have invested in a better GUI, and considered using a front end development framework
