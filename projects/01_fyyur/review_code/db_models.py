from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    # missing fields added - comment out in case need to rerun flask migrate (flask db init, flask db migrate)
    genres = db.Column(db.ARRAY(db.String(30)), nullable=False)
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, server_default='f', default=False)
    seeking_description = db.Column(db.String(250))

    def __repr__(self):
        return f'<Venue {self.id} {self.name} {self.city} {self.state} >'


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(30)), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    # missing fields added - comment out in case need to rerun flask migrate (flask db init, flask db migrate)
    # genres = db.Column(db.ARRAY(db.String(20)), nullable=False)
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, server_default='f', default=False)
    seeking_description = db.Column(db.String(250))

    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id', ondelete="CASCADE"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id', ondelete="CASCADE"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Show id: {self.id} Showtime {self.start_time}>'
