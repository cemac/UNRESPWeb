from flask import Flask, render_template, flash, redirect, url_for, request
from wtforms import Form, StringField, validators

app = Flask(__name__)
app.secret_key="TemporaryKey"

#Index
@app.route('/')
def index():
    return render_template('home.html')


#Gas experiences form
class GasExperiencesForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])

#Gas experiences
@app.route('/Gas_Experiences',methods=['GET', 'POST'])
def Gas_Experiences():
    form = GasExperiencesForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        flash('You successfully submitted the form', 'success')
        return redirect(url_for('Gas_Experiences'))
    return render_template('Gas_Experiences.html',form=form)

if __name__ == '__main__':
    app.run(debug=True)
