#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
from flask.scaffold import F
from flask_migrate import Migrate
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
from db_models import db, Artist, Show, Venue

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

    # call function to return venue list page data
    venues_list  = get_venue_list_page()

    # return render_template('pages/venues.html', areas=data);
    return render_template('pages/venues.html', areas=venues_list)


def get_venue_list_page():

    info = []

    locations = Venue.query.distinct(Venue.city,Venue.state).order_by("state","city").all()

    for location in locations: # get venues in the same city
        venues_data = []

        venues = Venue.query.filter_by(city=location.city, state=location.state).order_by("id").all()
        for venue in venues:  
            shows = Show.query.filter_by(venue_id=venue.id).all()
            upcoming_shows = 0
            for show in shows:
                upcoming_shows +=1 if show.start_time > current_time() else upcoming_shows

            # start populating venues_data
            venues_data.append({
              "id" : venue.id,
              "name": venue.name,
              "num_upcoming_shows": upcoming_shows
            })
        
        region = {
            "city": location.city,
            "state": location.state,
            "venues": venues_data
        }

        info.append(region)

    return info

@app.route('/venues/search', methods=['POST'])
def search_venues():
    
    search_string = request.form.get("search_term")
    venues = db.session.query(Venue).with_entities(Venue.id, Venue.name).filter(Venue.name.op("~*")(search_string)).all()
    
    venues_data = []

    for id, name in venues:

        venue_info = {
            "id": id,
            "name": name,
            "num_upcoming_shows": Show.query.filter_by(venue_id=id). \
                                             filter(Show.start_time>datetime.now()).count()
        }
        venues_data.append(venue_info)
    
    response = {
          "count": len(venues),
          "data": venues_data
    }

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

  venue_info = get_venue_info(venue_id)
  return render_template('pages/show_venue.html', venue=venue_info)


def current_time():
    return datetime.now()

def get_venue_info(venue_id):

    venue = Venue.query.get_or_404(venue_id)
    shows = Show.query.filter_by(venue_id=venue.id).all()

    past_shows, upcoming_shows = [], []
    past_shows_count, upcoming_shows_count = 0, 0

    for show in shows:
        
        artist=Artist.query.filter_by(id=show.artist_id).one()
        if show.start_time <= current_time():
            past_shows_count +=1
            past_rec = {
                "artist_id": artist.id,
                "artist_name": artist.name,
                "artist_image_link":  artist.image_link,
                "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            }
            past_shows.append(past_rec)
        else:
            upcoming_shows_count +=1
            upcoming_rec = {
                "artist_id": artist.id,
                "artist_name": artist.name,
                "artist_image_link":  artist.image_link,
                "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            }
            upcoming_shows.append(upcoming_rec)
  
    data={
      "id": venue_id,
      "name": venue.name,
      "genres": venue.genres,
      "address": venue.address,
      "city": venue.city,
      "state": venue.state,
      "phone": venue.phone,
      "website": venue.website_link,
      "facebook_link": venue.facebook_link,
      "seeking_talent": venue.seeking_talent,
      "seeking_description": venue.seeking_description,
      "image_link": venue.image_link,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
      "past_shows_count": past_shows_count,
      "upcoming_shows_count": upcoming_shows_count,
    }  

    return data

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

  form = VenueForm(request.form)

  venue = Venue(name=form.name.data,address=form.address.data,city=form.city.data,genres=form.genres.data,
                state=form.state.data,phone=form.phone.data,website_link=form.website_link.data,
                facebook_link=form.facebook_link.data,seeking_description=form.seeking_description.data,
                image_link=form.image_link.data,seeking_talent=form.seeking_talent.data)

  try:
    db.session.add(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  
  except:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  
  finally:
    db.session.close()

  # return render_template('pages/home.html')
  return redirect(url_for('venues'))

@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  venue = Venue.query.get_or_404(venue_id)
  
  try: 
    db.session.delete(venue)
    db.session.commit()
    flash('Venue ' + venue.name + ' and its associated shows deleted successfully.')

  except:
    flash('Venue ' + venue.name + ' delete request failed.')

  finally:
    db.session.close()
  
  # return None
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():

  data = []

  artists = Artist.query.order_by("id").all()

  for artist in artists:
      artist_record = {
          "id": artist.id,
          "name": artist.name,
      }
      data.append(artist_record)

  # return render_template('pages/artists.html', artists=data)
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():

    search_string = request.form.get("search_term")
    artists = db.session.query(Artist).with_entities(Artist.id, Artist.name).filter(Artist.name.op("~*")(search_string)).all()

    artists_data = []

    for id, name in artists:
  
        artist_info = {
            "id": id,
            "name": name,
            "num_upcoming_shows": Show.query.filter_by(artist_id=id). \
                                             filter(Show.start_time>current_time()).count()
        }
        artists_data.append(artist_info)
    
    response = {
          "count": len(artists),
          "data": artists_data
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

  artist = Artist.query.get_or_404(artist_id)
  past_artist_shows, upcoming_artist_shows = get_artist_shows(artist.id)

  data = {
   
      "id": artist.id,
      "name": artist.name,
      "genres": artist.genres,
      "city": artist.city,
      "state": artist.state,
      "phone": artist.phone,
      "website": artist.website_link,
      "facebook_link": artist.facebook_link,
      "seeking_venue": artist.seeking_venue,
      "seeking_description": artist.seeking_description,
      "image_link": artist.image_link,
      "past_shows": past_artist_shows,
      "upcoming_shows": upcoming_artist_shows,
      "past_shows_count": Show.query.filter_by(artist_id=artist.id).filter(Show.start_time<=current_time()).count(),
      "upcoming_shows_count": Show.query.filter_by(artist_id=artist.id).filter(Show.start_time>current_time()).count(),
  }

  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)


def get_artist_shows(artist_id):

    past_shows, upcoming_shows = [], []

    past = db.session.query(Venue.id, Venue.name, Venue.image_link, Show.start_time).\
                            select_from(Show).join(Artist).join(Venue).\
                            filter(Show.artist_id==artist_id, Show.start_time <= current_time()).all()
        
    upcoming = db.session.query(Venue.id, Venue.name, Venue.image_link, Show.start_time).\
                                select_from(Show).join(Artist).join(Venue).\
                                filter(Show.artist_id==artist_id, Show.start_time > current_time()).all()

    if past:
          for venue_id, venue_name, venue_image_link, show_start_time in past:
              past_rec = {
                "venue_id": venue_id,
                "venue_name": venue_name,
                "venue_image_link":  venue_image_link,
                "start_time": show_start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
              }
              past_shows.append(past_rec)
        
    if upcoming:
          for venue_id, venue_name, venue_image_link, show_start_time in upcoming:
            upcoming_rec = {
                "venue_id": venue_id,
                "venue_name": venue_name,
                "venue_image_link":  venue_image_link,
                "start_time": show_start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            }
            upcoming_shows.append(upcoming_rec)

    return past_shows, upcoming_shows


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  
  artist = Artist.query.get_or_404(artist_id)

  # TODO: populate form with fields from artist with ID <artist_id>
  form = ArtistForm(obj=artist)

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  form = ArtistForm(request.form)

  artist = Artist.query.get_or_404(artist_id)
  form.populate_obj(artist)

  try:
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
  except:
    flash('Artist ' + request.form['name'] + ' profile update failed.')

  finally:
    db.session.close()
  
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  venue = Venue.query.get_or_404(venue_id)
  # automatically fill the form with the data retrieved
  form = VenueForm(obj=venue)  

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

  form = VenueForm(request.form)
  venue = Venue.query.get_or_404(venue_id)
  form.populate_obj(venue)
  try:
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully updated.')
  except:
    flash('Venue ' + request.form['name'] + ' update failed.')
  finally:
    db.session.close()


  return redirect(url_for('show_venue', venue_id=venue_id))
  
#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Artist record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form)

  artist = Artist(name=form.name.data,city=form.city.data,genres=form.genres.data,state=form.state.data,phone=form.phone.data,
                  website_link=form.website_link.data,facebook_link=form.facebook_link.data,seeking_venue=form.seeking_venue.data,
                  seeking_description=form.seeking_description .data,image_link=form.image_link.data)
  
  try:
    db.session.add(artist)
    db.session.commit()
  # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed.')
  
  except:
    flash('Artist creation failed.')
  
  finally:
    db.session.close()

  return render_template('pages/home.html')
  

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  show_data = []

  # the proper way to do joins with SQLAlchemy
  # the only way for this to work is for Show table to establish relationship with Venue and Artist tables
  
  # the following query pulls only upcoming shows (i.e. Show.start_time > current timestamp -  see filter setup in query below)
  results = db.session.query(Venue.id, Venue.name, Artist.id, Artist.name, Artist.image_link, Show.start_time).\
                             select_from(Show).join(Venue).join(Artist).\
                             filter(Show.start_time > current_time()).\
                             order_by(Show.start_time).all()
                             
  for venue_id, venue_name, artist_id, artist_name, image_link, start_time in results:
      rec = {
        "venue_id": venue_id,
        "venue_name": venue_name,
        "artist_id": artist_id,
        "artist_name": artist_name,
        "artist_image_link": image_link,
        "start_time": str(start_time)
      }
      show_data.append(rec)

  return render_template('pages/shows.html', shows=show_data)


#  Create Show
#  ----------------------------------------------------------------
@app.route('/shows/create', methods=['GET'])
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  form = ShowForm(request.form)
  show = Show(artist_id=form.artist_id.data,
              venue_id=form.venue_id.data,
              start_time=form.start_time.data)

  try:
    db.session.add(show)
    db.session.commit()

    # on successful db insert, flash success
    flash('Show id ' + str(show.id) + ' was successfully listed!')

  except:
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0',port=5000,threaded=False)
# '''
