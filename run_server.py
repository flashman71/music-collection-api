import os
from server import create_app
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def init(self):
    if __name__ == '__main__':
        env_name = os.getenv('FLASK_ENV')
        app = create_app(env_name)
        # run app
        app.run()
