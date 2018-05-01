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

#Set subdomain...
#If running locally (or index is the domain) set to blank, i.e. subd=""
#If index is a subdomain, set as appropriate *including* leading slash, e.g. subd="/vumo-data"
#Routes in @app.route() should NOT include subd, but all other references should...
#Use redirect(subd + '/route') rather than redirect(url_for(route))
#Pass subd=subd into every render_template so that it can be used to set the links appropriately
#
subd="/vumo-data"

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
    supported_languages = ["en", "es"]
    try:
        lang = request.accept_languages.best_match(supported_languages)
    except:
        lang = "es"
    if(lang=="en"):
        return redirect(subd+'/en')
    else:
        return redirect(subd+'/es')

#Home
@app.route('/en')
def Home():
    return render_template('home.html',subd=subd)

#Home (es)
@app.route('/es')
def Home_es():
    return render_template('home-es.html',subd=subd)

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
    latitude=DecimalField('Latitude',[validators.NumberRange(min=10,max=16,message="Latitude out of bounds")])
    longitude=DecimalField('Longitude',[validators.NumberRange(min=-88,max=-82,message="Longitude out of bounds")])

#Gas experiences form (es)
class GasExperiencesFormEs(Form):
    date = DateField('Fecha de la experiencia',
       [validators.DataRequired(message="No es una fecha válida")],format='%Y-%m-%d')
    smell = RadioField('¿Usted sintió el olor del vumo?',
       [validators.InputRequired(message="No es una selección válida")],
       choices=[('Yes','Sí'),('No','No')])
    throat = RadioField('¿Usted sintió el vumo en la garganta? Por ejemplo, ardor o prurito',
       [validators.InputRequired(message="No es una selección válida")],
       choices=[('Yes','Sí'),('No','No')])
    eyes = RadioField('¿Usted sintió el vumo en los ojos? Por ejemplo, ardor o prurito',
       [validators.InputRequired(message="No es una selección válida")],
       choices=[('Yes','Sí'),('No','No')])
    skin = RadioField('¿Usted sintió el vumo en la piel? Por ejemplo, ardor o prurito',
       [validators.InputRequired(message="No es una selección válida")],
       choices=[('Yes','Sí'),('No','No')])
    tired = RadioField('¿El vumo le hizo sentir inusualmente cansado/a?',
       [validators.InputRequired(message="No es una selección válida")],
       choices=[('Yes','Sí'),('No','No')])
    nausea = RadioField('¿El vumo le provocó náuseas?',
       [validators.InputRequired(message="No es una selección válida")],
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
       ('Strong wind', 'Viento fuerte'), ('Very strong wind', 'Viento muy fuerte'), ("Dont know", "No se sabe")])
    precip=SelectField('¿Había lluvia cuando se sintió el vumo?',\
       [validators.NoneOf(('blank'),message='Por favor seleccione')],\
       choices=[('blank','--Por favor seleccione--'),('No precipitation', 'No había lluvia'), ('Light rain', 'Lluvia ligera'),\
       ('Rain', 'Lluvia'),("Dont know", "No se sabe")])
    latitude=DecimalField('Latitud',[validators.NumberRange(min=10,max=16,message="Latitud fuera de límites")])
    longitude=DecimalField('Longitud',[validators.NumberRange(min=-88,max=-82,message="Longitud fuera de límites")])

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
        return redirect(subd+'/Questionnaire')
    return render_template('Gas_Experiences.html',form=form,subd=subd)

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
        return redirect(subd+'/Encuesta')
    return render_template('Gas_Experiences-es.html',form=form,subd=subd)

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

#Gas experiences map form (es)
class GasExperiencesMapEs(Form):
    question = SelectField('Ver respuestas a la pregunta:',\
       choices=[('sense',"¿Usted sintió el vumo? (i.e. 'Sí' a cualquier pregunta)"),\
       ('smell','¿Usted sintió el olor del vumo?'),('throat', '¿Usted sintió el vumo en la garganta?'),\
       ('eyes', '¿Usted sintió el vumo en los ojos?'), ('skin', '¿Usted sintió el vumo en la piel?'),\
       ('tired', '¿El vumo le hizo sentir inusualmente cansado/a?'), ('nausea', '¿El vumo le provocó náuseas?')])
    windDir = SelectField('Dirección del viento:',\
       choices=[('any','Cualquier'),('N', 'Norte'), ('NE', 'Noreste'),\
       ('E', 'Este'), ('SE', 'Sudeste'), ('S', 'Sur'), ('SW', 'Sudoeste'),\
       ('W', 'Oeste'), ('NW', 'Noroeste')])
    windSpeed = SelectField('Velocidad del viento:',\
       choices=[('any','Cualquier'),('No wind', 'No había viento'), ('Slow wind', 'No muy fuerte'),\
       ('Strong wind', 'Viento fuerte'), ('Very strong wind', 'Viento muy fuerte')])
    precip = SelectField('Lluvia:',\
       choices=[('any','Cualquier'),('No precipitation', 'No había lluvia'), ('Light rain', 'Lluvia ligera'),\
        ('Rain', 'Lluvia')])

#Gas experiences maps
@app.route('/Maps',methods=['GET', 'POST'])
def Maps():
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
    return render_template('form_maps.html',subData=subData,question=question,form=form,subd=subd)

#Function to translate database answers to Spanish
def translateDB(subData):
    for index, row in subData.iterrows():
        #Translate Yes/No fields:
        for field in ["smell","throat","eyes","skin","tired","nausea"]:
            if row[field] == "Yes":
                subData.loc[index,field] = "Sí"
        #Translate wind direction field:
        if row["windDir"] == "Dont know":
            subData.loc[index,"windDir"] = "No se sabe"
        #Translate wind speed field:
        if row["windSpeed"] == "No wind":
            subData.loc[index,"windSpeed"] = "No había viento"
        elif row["windSpeed"] == "Slow wind":
            subData.loc[index,"windSpeed"] = "No muy fuerte"
        elif row["windSpeed"] == "Strong wind":
            subData.loc[index,"windSpeed"] = "Viento fuerte"
        elif row["windSpeed"] == "Very strong wind":
            subData.loc[index,"windSpeed"] = "Viento muy fuerte"
        elif row["windSpeed"] == "Dont know":
            subData.loc[index,"windSpeed"] = "No se sabe"
        #Translate precipitation field:
        if row["precip"] == "No precipitation":
            subData.loc[index,"precip"] = "No había lluvia"
        elif row["precip"] == "Light rain":
            subData.loc[index,"precip"] = "Lluvia ligera"
        elif row["precip"] == "Rain":
            subData.loc[index,"precip"] = "Lluvia"
        elif row["precip"] == "Dont know":
            subData.loc[index,"precip"] = "No se sabe"
    return subData

#Gas experiences maps (es)
@app.route('/Mapas',methods=['GET', 'POST'])
def Mapas():
    form = GasExperiencesMapEs(request.form)
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
    subDataEs = translateDB(subData)
    return render_template('form_maps-es.html',subData=subDataEs,question=question,form=form)

#Feedback form
class FeedbackForm(Form):
    feedback = TextAreaField('Feedback:',[validators.Length(min=1, max=5000)])

#Feedback form (es)
class FeedbackFormEs(Form):
    feedback = TextAreaField('Comentarios:',
       [validators.Length(min=1, max=5000, message="Entre 1 y 5000 caracteres solamente")])

#feedback
@app.route('/Feedback',methods=['GET', 'POST'])
def Feedback():
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
        return redirect(subd+'/Feedback')
    return render_template('feedback.html',form=form,subd=subd)

#feedback (es)
@app.route('/Comentarios',methods=['GET', 'POST'])
def Comentarios():
    form = FeedbackFormEs(request.form)
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
        flash('Enviaste con éxito los comentarios', 'success')
        return redirect(subd+'/Comentarios')
    return render_template('feedback-es.html',form=form,subd=subd)

if __name__ == '__main__':
    app.run()
