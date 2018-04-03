from flask import Flask, render_template, flash, redirect, url_for, request, g
from wtforms import Form, DecimalField, TextAreaField, RadioField, SelectField, validators
from wtforms.fields.html5 import DateField
import datetime as dt
import sqlite3
import os
import pandas as pd

app = Flask(__name__)
assert os.path.exists('AppSecretKey.txt'), "Unable to locate app secret key"
with open('AppSecretKey.txt','r') as f:
    key=f.read()
app.secret_key=key
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

#Query DB pandas
def pandas_db(query):
    db = get_db()
    df = pd.read_sql_query(query,db)
    db.close()
    return df

#Index
@app.route('/')
def index():
    return render_template('home.html')

#Index (es)
@app.route('/es')
def index_es():
    return render_template('home-es.html')

#Gas experiences form
class GasExperiencesForm(Form):
    date = DateField('Date of experience',format='%Y-%m-%d')
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
       ('E', 'East'), ('SE', 'Southeast'), ('S', 'South'), ('SW', 'Southwest'),\
       ('W', 'West'), ('NW', 'Northwest'), ("Dont know", "Don't know")])
    windSpeed = SelectField('How strong was the wind when you felt the vumo?',\
       [validators.NoneOf(('blank'),message='Please select')],\
       choices=[('blank','--Please select--'),('No wind', 'No wind'), ('Slow wind', 'Slow wind'),\
       ('Strong wind', 'Strong wind'), ('Very strong wind', 'Very strong wind'), ("Dont know", "Don't know")])
    precip=SelectField('Was there any precipitation when you felt the vumo?',\
       [validators.NoneOf(('blank'),message='Please select')],\
       choices=[('blank','--Please select--'),('No precipitation', 'No precipitation'), ('Light rain', 'Light rain'),\
       ('Rain', 'Rain'),("Dont know", "Don't know")])
    latitude=DecimalField('latitude',[validators.NumberRange(min=10,max=16,message="latitude out of bounds")])
    longitude=DecimalField('longitude',[validators.NumberRange(min=-88,max=-82,message="longitude out of bounds")])

#Gas experiences form (es)
class GasExperiencesFormEs(Form):
    date = DateField('Fecha de la experiencia',format='%Y-%m-%d')
    smell = RadioField('¿Usted sintió el olor del vumo?', choices=[('Yes','Sí'),('No','No')])
    throat = RadioField('¿Usted sintió el vumo en la garganta? Por ejemplo, ardor o prurito',\
       choices=[('Yes','Sí'),('No','No')])
    eyes = RadioField('¿Usted sintió el vumo en los ojos? Por ejemplo, ardor o prurito',\
       choices=[('Yes','Sí'),('No','No')])
    skin = RadioField('¿Usted sintió el vumo en la piel? Por ejemplo, ardor o prurito',\
       choices=[('Yes','Sí'),('No','No')])
    tired = RadioField('¿El vumo le hizo sentir inusualmente cansado/a?',\
       choices=[('Yes','Sí'),('No','No')])
    nausea = RadioField('¿El vumo le provocó náuseas?',\
       choices=[('Yes','Sí'),('No','No')])
    otherObs = TextAreaField('¿Podía ver el vumo? ¿Cómo se veía?\
       Por ejemplo el color, la visibilidad. Para cualquier observación, puede escribir en este espacio',\
       [validators.Length(min=0, max=500)])
    windDir = SelectField('¿De dónde venía el viento cuando se sintió el vumo?',\
       [validators.NoneOf(('blank'),message='Por favor seleccione')],\
       choices=[('blank','--Por favor seleccione--'),('N', 'Norte'), ('NE', 'Noreste'),\
       ('E', 'Este'), ('SE', 'Sudeste'), ('S', 'Sur'), ('SW', 'Sudoeste'),\
       ('W', 'Oeste'), ('NW', 'Noroeste'), ("Dont know", "No se sabe")])
    windSpeed = SelectField('¿Cómo era de fuerte el viento?',\
       [validators.NoneOf(('blank'),message='Por favor seleccione')],\
       choices=[('blank','--Por favor seleccione--'),('No wind', 'No había viento'), ('Slow wind', 'No muy fuerte'),\
       ('Strong wind', 'viento fuerte'), ('Very strong wind', 'viento muy fuerte'), ("Dont know", "no se sabe")])
    precip=SelectField('¿Había lluvia cuando se sintió el vumo?',\
       [validators.NoneOf(('blank'),message='Por favor seleccione')],\
       choices=[('blank','--Por favor seleccione--'),('No precipitation', 'No había lluvia'), ('Light rain', 'lluvia ligera'),\
       ('Rain', 'lluvia'),("Dont know", "no se sabe")])
    latitude=DecimalField('latitud',[validators.NumberRange(min=10,max=16,message="latitud fuera de límites")])
    longitude=DecimalField('longitud',[validators.NumberRange(min=-88,max=-82,message="longitud fuera de límites")])

#Questionnaire
@app.route('/Questionnaire',methods=['GET', 'POST'])
def Questionnaire():
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
        latitude = float(form.latitude.data)
        longitude = float(form.longitude.data)
        if smell=='Yes' or throat=='Yes' or eyes=='Yes' or skin=='Yes' or tired=='Yes' or nausea=='Yes':
            sense = 'Yes'
        else:
            sense = 'No'

        ###Insert into database:
        #Create cursor
        db = get_db()
        cur = db.cursor()
        #Execute query:
        cur.execute("INSERT INTO Experiences(date,sense,smell,throat,eyes,skin,tired,nausea,otherObs,windDir,windSpeed,precip,latitude,longitude)\
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (date,sense,smell,throat,eyes,skin,tired,nausea,otherObs,windDir,windSpeed,precip,latitude,longitude))
        #Commit to DB
        db.commit()
        #Close connection
        cur.close()

        flash('You successfully submitted the questionnaire', 'success')
        return redirect(url_for('Questionnaire'))
    return render_template('Gas_Experiences.html',form=form)

#Questionnaire (es)
@app.route('/Encuesta',methods=['GET', 'POST'])
def Questionnaire_Es():
    form = GasExperiencesFormEs(request.form)
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
        latitude = float(form.latitude.data)
        longitude = float(form.longitude.data)
        if smell=='Yes' or throat=='Yes' or eyes=='Yes' or skin=='Yes' or tired=='Yes' or nausea=='Yes':
            sense = 'Yes'
        else:
            sense = 'No'

        ###Insert into database:
        #Create cursor
        db = get_db()
        cur = db.cursor()
        #Execute query:
        cur.execute("INSERT INTO Experiences(date,sense,smell,throat,eyes,skin,tired,nausea,otherObs,windDir,windSpeed,precip,latitude,longitude)\
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (date,sense,smell,throat,eyes,skin,tired,nausea,otherObs,windDir,windSpeed,precip,latitude,longitude))
        #Commit to DB
        db.commit()
        #Close connection
        cur.close()

        flash('Enviaste con éxito la encuesta', 'success')
        return redirect(url_for('Questionnaire_Es'))
    return render_template('Gas_Experiences-es.html',form=form)

#Gas experiences map form
class GasExperiencesMap(Form):
    question = SelectField('Show answers to the question:',\
       choices=[('sense',"Could you sense the vumo (i.e. any questions answered 'Yes')?"),\
       ('smell','Could you smell the vumo?'),('throat', 'Could you feel the vumo in your throat?'),\
       ('eyes', 'Could you feel the vumo in your eyes?'), ('skin', 'Could you feel the vumo on your skin?'),\
       ('tired', 'Did the vumo make you unusually tired?'), ('nausea', 'Did the vumo make you feel nauseous?')])
    windDir = SelectField('For wind direction:',\
       choices=[('any','Any'),('N', 'North'), ('NE', 'Northeast'),\
       ('E', 'East'), ('SE', 'Southeast'), ('S', 'South'), ('SW', 'Southwest'),\
       ('W', 'West'), ('NW', 'Northwest')])
    windSpeed = SelectField('wind speed:',\
       choices=[('any','Any'),('No wind', 'No wind'), ('Slow wind', 'Slow wind'),\
       ('Strong wind', 'Strong wind'), ('Very strong wind', 'Very strong wind')])
    precip = SelectField('and precipitation:',\
       choices=[('any','Any'),('No precipitation', 'No precipitation'), ('Light rain', 'Light rain'),\
        ('Rain', 'Rain')])

#Gas experiences maps
@app.route('/form_maps',methods=['GET', 'POST'])
def form_maps():
    form = GasExperiencesMap(request.form)
    subData = pandas_db('SELECT * FROM Experiences')
    if request.method == 'POST':
        question = form.question.data
        #Subset by wind direction:
        if form.windDir.data != 'any':
            subData = subData[subData['windDir']==form.windDir.data]
        #Subset by wind speed:
        if form.windSpeed.data != 'any':
            subData = subData[subData['windSpeed']==form.windSpeed.data]
        #Subset by precip:
        if form.precip.data != 'any':
            subData = subData[subData['precip']==form.precip.data]
    else:
        question = 'sense'

    return render_template('form_maps.html',subData=subData,question=question,form=form)

#Feedback form
class FeedbackForm(Form):
    feedback = TextAreaField('Feedback:',[validators.Length(min=0, max=5000)])

#feedback
@app.route('/feedback',methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm(request.form)
    if request.method == 'POST' and form.validate():
        feedback=form.feedback.data
        ###Insert into database:
        #Create cursor
        db = get_db()
        cur = db.cursor()
        #Execute query:
        cur.execute("INSERT INTO Feedback(feedback) VALUES(?)", (feedback,))
        #Commit to DB
        db.commit()
        #Close connection
        cur.close()
        flash('You successfully submitted the feedback form', 'success')
        return redirect(url_for('feedback'))
    return render_template('feedback.html',form=form)

if __name__ == '__main__':
    app.run()
