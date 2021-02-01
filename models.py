from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from config import db, ma, Configvalues

'''
   Title........: models.py
   Description..: Defines database table/view models to be used by SQLAlchemy
   Dependencies.: sqlalchemy, sqlalchemy.orm, config
'''
class Artist(db.Model):
    __table_args__ = {
        'schema': Configvalues.SCHEMA  
    }
    __tablename__ = 'artists_$t'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    mbid = db.Column(db.String, nullable=False)
    date_created = db.Column(db.String, nullable=False)
    app_created = db.Column(db.String, nullable=False)
    date_updated = db.Column(db.String, nullable=False)
    app_updated = db.Column(db.String, nullable=False)


class ArtistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Artist
        fields = ('id', 'name', 'mbid', 'date_created', 'app_created', 'date_updated', 'app_updated')
        sqla_session = db.session
        include_fk = True


class AlbumView(db.Model):
    __table_args__ = {
        'schema': Configvalues.SCHEMA  
    }
    __tablename__ = 'album_view'

    artist_id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String, nullable=False)
    album_name = db.Column(db.String, nullable=False)


class AlbumViewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AlbumView
        fields = ('artist_name', 'album_name')


class Album(db.Model):
    __table_args__ = {
        'schema': Configvalues.SCHEMA  
    }

    __tablename__ = 'albums_$t'
    id = db.Column(db.Integer, primary_key=True)
    album_name = db.Column(db.String, nullable=False)
    artist_id = db.Column(db.Integer, ForeignKey(Artist.id))
    artist_name = relationship("Artist", primaryjoin="Album.artist_id==Artist.id")
    date_created = db.Column(db.String, nullable=False)
    app_created = db.Column(db.String, nullable=False)
    date_updated = db.Column(db.String, nullable=False)
    app_updated = db.Column(db.String, nullable=False)


class AlbumSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Album
        fields = ('id', 'album_name', 'artist_name', 'date_created', 'app_created', 'date_updated', 'app_updated')
        sqla_session = db.session
        include_fk = True


class Track(db.Model):
    __table_args__ = {
        'schema': Configvalues.SCHEMA  
    }

    __tablename__ = 'tracks_$t'
    id = db.Column(db.Integer, primary_key=True)
    track_name = db.Column(db.String, nullable=False)
    album_id = db.Column(db.Integer, primary_key=False)
    date_created = db.Column(db.String, nullable=False)
    app_created = db.Column(db.String, nullable=False)
    date_updated = db.Column(db.String, nullable=False)
    app_updated = db.Column(db.String, nullable=False)


class TrackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Track
        fields = ('id', 'track_name', 'album_id', 'date_created', 'app_created', 'date_updated', 'app_updated')
        sqla_session = db.session
        include_fk = True


class TrackView(db.Model):
    __table_args__ = {
        'schema': Configvalues.SCHEMA
    }
    __tablename__ = 'track_view'

    artist_id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String, nullable=False)
    album_name = db.Column(db.String, nullable=False)
    track_name = db.Column(db.String, nullable=False)


class TrackViewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrackView
        fields = ('artist_name', 'album_name', 'track_name')
