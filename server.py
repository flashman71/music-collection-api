from flask import Flask
from flask import request
from flask_cors import CORS
from models import Artist, TrackView, TrackViewSchema, ArtistSchema, AlbumView, AlbumViewSchema
import os

'''
   Title........: server.py
   Description..: Main program
                  API routes are defined and accessed 
   Dependencies.: flask, flask_cors, models, os
   APIs.........:
                  /artist
                     GET, POST
                     JSON Input/ JSON Output
                  /album
                     GET, POST
                     JSON Input/ JSON Output
                  /track
                     GET, POST
                     JSON Input/ JSON Output
'''

# Define the environment to use
env_name = os.getenv('FLASK_ENV')


# create_app --This is the main function in this file.  It will create
#              a Flask app.  CORS is used to allow cross-site access
def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route("/favicon.ico")
    def favicon():
        return "", 200

# Route for index
    @app.route('/', methods=['GET'])
    def index():
        return "Index endpoint for API"

    @app.route('/artist', methods=['GET', 'POST'])
    def get_artist():
        if request.is_json:
            req = request.get_json()
            artist_name = req['artist_name']
            if "filter_type" not in req:
                print("filter_type not provided")
                filter_value = (Artist.name == artist_name)
            else:
                filter_type = req['filter_type']
                if filter_type == "Ends With":
                    filter_value = (Artist.name.endswith(artist_name))
                elif filter_type == "Starts With":
                    filter_value = (Artist.name.startswith(artist_name))
                else:
                    filter_value = (Artist.name == artist_name)

            artist_output = Artist.query.filter(filter_value).all()
            artist_schema = ArtistSchema(many=True)
            response = app.response_class(
                response=artist_schema.dumps(artist_output),
                status=200,
                content_type='application/json'
            )
            return response
        else:
            return "Artist endpoint, invalid input, not JSON", 404

    @app.route('/album', methods=['GET', 'POST'])
    def get_albums():
        if request.is_json:
            req = request.get_json()
            if "album_name" not in req and "artist_name" not in req:
                return "Album search, invalid input data", 400

            if "filter_type" in req:
                filter_type = req['filter_type']
            else:
                filter_type = "Equals"

            use_artist = 0
            use_album = 0
            if "album_name" in req:
                use_album = 1
                album_name = req['album_name']
                print("Querying album_name: ", album_name)
                if filter_type == "Equals":
                    filter_value = (AlbumView.album_name == album_name)
                elif filter_type == "Ends With":
                    filter_value = (AlbumView.album_name.endswith(album_name))
                elif filter_type == "Starts With":
                    filter_value = (AlbumView.album_name.startswith(album_name))

            if "artist_name" in req:
                use_artist = 1
                artist_name = req['artist_name']
                print("Querying artist name: ", artist_name)
                if filter_type == "Ends With":
                    filter_value2 = (AlbumView.artist_name.endswith(artist_name))
                elif filter_type == "Starts With":
                    filter_value2 = (AlbumView.artist_name.startswith(artist_name))
                else:
                    filter_value2 = (AlbumView.artist_name == artist_name)

            if use_artist == 1 and use_album == 1:
                album_output = AlbumView.query.filter(filter_value).filter(filter_value2).all()
            elif use_artist == 1 and use_album == 0:
                album_output = AlbumView.query.filter(filter_value2).all()
            else:
                album_output = AlbumView.query.filter(filter_value).all()

            album_schema = AlbumViewSchema(many=True)
            response = app.response_class(
                response=album_schema.dumps(album_output),
                status=200,
                mimetype='application/json'
            )
            return response
        else:
            return "Album endpoint, invalid input, not JSON", 404

    @app.route('/track', methods=['GET', 'POST'])
    def get_tracks():
        if request.is_json:
            req = request.get_json()
            use_track = 0
            use_album = 0
            use_artist = 0

            if "filter_type" not in req:
                filter_type = "Equals"
            else:
                filter_type = req['filter_type']

            if "track_name" not in req and "album_name" not in req and "artist_name" not in req:
                return "Track endpoint, Input data is invalid", 400

            if "track_name" in req:
                use_track = 1
                track_name = req["track_name"]
                if filter_type == "Ends With":
                    filter_value = (TrackView.track_name.endswith(track_name))
                elif filter_type == "Starts With":
                    filter_value = (TrackView.track_name.startswith(track_name))
                else:
                    filter_value = (TrackView.track_name == track_name)

            if "album_name" in req:
                use_album = 1
                album_name = req["album_name"]
                if filter_type == "Ends With":
                    filter_value2 = (TrackView.album_name.endswith(album_name))
                elif filter_type == "Starts With":
                    filter_value2 = (TrackView.album_name.startswith(album_name))
                else:
                    filter_value2 = (TrackView.album_name == album_name)

            if "artist_name" in req:
                use_artist = 1
                artist_name = req["artist_name"]
                if filter_type == "Ends With":
                    filter_value3 = (TrackView.artist_name.endswith(artist_name))
                elif filter_type == "Starts With":
                    filter_value3 = (TrackView.artist_name.startswith(artist_name))
                else:
                    filter_value3 = (TrackView.artist_name == artist_name)

            if use_track == 1 and use_album == 0 and use_artist == 0:
                track_output = TrackView.query.filter(filter_value).all()
            elif use_track == 0 and use_album == 1 and use_artist == 0:
                track_output = TrackView.query.filter(filter_value2).all()
            elif use_track == 0 and use_album == 0 and use_artist == 1:
                track_output = TrackView.query.filter(filter_value3).all()
            elif use_track == 1 and use_album == 1 and use_artist == 0:
                track_output = TrackView.query.filter(filter_value).filter(filter_value2).all()
            elif use_track == 1 and use_album == 0 and use_artist == 1:
                track_output = TrackView.query.filter(filter_value).filter(filter_value3).all()
            elif use_track == 0 and use_album == 1 and use_artist == 1:
                track_output = TrackView.query.filter(filter_value2).filter(filter_value3).all()
            else:
                track_output = TrackView.query.filter(filter_value).filter(filter_value2).filter(filter_value3).all()

            track_schema = TrackViewSchema(many=True)
            response = app.response_class(
                response=track_schema.dumps(track_output),
                status=200,
                mimetype='application/json'
            )
            return response
        else:
            return "Track endpoint, invalid input, not JSON", 404

    if __name__ == '__main__':
        app.run()

    return app
