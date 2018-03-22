from flask import Flask, render_template, flash, redirect, url_for, request, g
from wtforms import Form, TextAreaField, RadioField, SelectField, validators
from wtforms.fields.html5 import DateField
import datetime as dt
import sqlite3
import os
from flask_googlemaps import GoogleMaps

app = Flask(__name__)
app.secret_key="TemporaryKey"
app.config['GOOGLEMAPS_KEY']="AIzaSyDnw_sLdaNZLt05my-efZ5i-AM-u97GQBw"
GoogleMaps(app)
DATABASE = 'UNRESPWeb.db'
assert os.path.exists(DATABASE), "Unable to locate database"

#Connect to DB
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

#Close DB if app stops
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#Query DB
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else (rv if rv else None)

#Index
@app.route('/')
def index():
    return render_template('home.html')

#Gas experiences form
class GasExperiencesForm(Form):
    date = DateField('Date',format='%Y-%m-%d')
    smell = RadioField('Could you smell the vumo?', choices=[('Yes','Yes'),('No','No')])
    throat = RadioField('Could you feel the vumo in your throat? For example burning or itching',\
       choices=[('Yes','Yes'),('No','No')])
    eyes = RadioField('Could you feel the vumo in your eyes? For example burning or itching',\
       choices=[('Yes','Yes'),('No','No')])
    skin = RadioField('Could you feel the vumo on your skin? For example burning or itching',\
       choices=[('Yes','Yes'),('No','No')])
    tired = RadioField('Did the vumo make you unusually tired?',\
       choices=[('Yes','Yes'),('No','No')])
    nausea = RadioField('Did the vumo make you feel nauseous?',\
       choices=[('Yes','Yes'),('No','No')])
    otherObs = TextAreaField('Could you see the vumo? What did it look like?\
       For example colour, visibility. You can write any other observations in this box',\
       [validators.Length(min=0, max=500)])
    windDir = SelectField('Where was the wind coming from when you felt the vumo?',\
       [validators.NoneOf(('blank'),message='Please select')],\
       choices=[('blank','--Please select--'),('N', 'North'), ('NE', 'Northeast'),\
       ('E', 'East'), ('SE', 'SouthEast'), ('S', 'South'), ('SW', 'Southwest'),\
       ('W', 'West'), ('NW', 'Northwest'), ("Don't know", "Don't know")])
    windSpeed = SelectField('How strong was the wind when you felt the vumo?',\
       [validators.NoneOf(('blank'),message='Please select')],\
       choices=[('blank','--Please select--'),('No wind', 'No wind'), ('Slow wind', 'Slow wind'),\
       ('Strong wind', 'Strong wind'), ('Very strong wind', 'Very strong wind'), ("Don't know", "Don't know")])
    precip=SelectField('Was there any precipitation when you felt the vumo?',\
       [validators.NoneOf(('blank'),message='Please select')],\
       choices=[('blank','--Please select--'),('No precipitation', 'No precipitation'), ('Light rain', 'Light rain'),\
       ('Rain', 'Rain'),("Don't know", "Don't know")])

#Gas experiences
@app.route('/Gas_Experiences',methods=['GET', 'POST'])
def Gas_Experiences():
    form = GasExperiencesForm(request.form)
    if request.method == 'POST' and form.validate():
        date = form.date.data
        smell = form.smell.data
        throat = form.throat.data
        eyes = form.eyes.data
        skin = form.skin.data
        tired = form.tired.data
        nausea = form.nausea.data
        otherObs = form.otherObs.data
        windDir = form.windDir.data
        windSpeed = form.windSpeed.data
        precip = form.precip.data

        ###Insert into database:
        #Create cursor
        db = get_db()
        cur = db.cursor()
        #Execute query:
        cur.execute("INSERT INTO Experiences(date,smell,throat,eyes,skin,tired,nausea,otherObs,windDir,windSpeed,precip) VALUES(?,?,?,?,?,?,?,?,?,?,?)", (date,smell,throat,eyes,skin,tired,nausea,otherObs,windDir,windSpeed,precip))
        #Commit to DB
        db.commit()
        #Close connection
        cur.close()

        flash('You successfully submitted the form', 'success')
        return redirect(url_for('Gas_Experiences'))
    return render_template('Gas_Experiences.html',form=form)

if __name__ == '__main__':
    app.run(debug=True)
