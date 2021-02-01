from flask import Flask
import connexion
import os
import csv
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))


class Configvalues:
    DB_URI = ""
    SCHEMA = ""

    with open("api_config.env") as infile:
        for row in csv.reader(infile, delimiter="="):
            if row[0] == 'DB_URI':
                DB_URI = row[1]

            if row[0] == "SCHEMA":
                SCHEMA = row[1]


# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app
app = Flask(__name__)

# Set the database connection string
app.config['SQLALCHEMY_DATABASE_URI'] = Configvalues.DB_URI  
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
