from flask import Flask, render_template, flash, redirect, url_for, request
from wtforms import Form, StringField, RadioField, SelectField, validators
from wtforms.fields.html5 import DateField
import datetime as dt

app = Flask(__name__)
app.secret_key="TemporaryKey"

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
    otherObs = StringField('Could you see the vumo? What did it look like?\
       For example colour, visibility. You can write any other observations in this box',\
       [validators.Length(min=0, max=500)])
    windDir = SelectField('Where was the wind coming from when you felt the vumo?',\
       [validators.NoneOf(('blank'),message='Please select')],\
       choices=[('blank','--Please select--'),('N', 'North'), ('NE', 'Northeast'),\
       ('E', 'East'), ('SE', 'SouthEast'), ('S', 'South'), ('SW', 'Southwest'),\
       ('W', 'West'), ('NW', 'Northwest'), ('DK', "Don't know")])
    windSpeed = SelectField('How strong was the wind when you felt the vumo?',\
       [validators.NoneOf(('blank'),message='Please select')],\
       choices=[('blank','--Please select--'),('No', 'No wind'), ('Slow', 'Slow wind'),\
       ('Strong', 'Strong wind'), ('VStrong', 'Very strong wind'), ('DK', "Don't know")])
    precip=SelectField('Was there any precipitation when you felt the vumo?',\
       [validators.NoneOf(('blank'),message='Please select')],\
       choices=[('blank','--Please select--'),('No', 'No precipitation'), ('Light', 'Light rain'),\
       ('Rain', 'Rain'),('DK', "Don't know")])

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
        flash('You successfully submitted the form', 'success')
        return redirect(url_for('Gas_Experiences'))
    return render_template('Gas_Experiences.html',form=form)

if __name__ == '__main__':
    app.run(debug=True)
