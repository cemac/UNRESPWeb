from flask import Flask, render_template, flash

app = Flask(__name__)
app.secret_key="TemporaryKey"

#Index
@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
