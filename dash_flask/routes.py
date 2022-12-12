from flask import current_app as app
from flask import render_template

@app.route('/')
def ola():
    return render_template('index.html')