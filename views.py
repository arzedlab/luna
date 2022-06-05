import imp
from app import app
from flask import render_template

@app.route('/')
def home_page():
    return render_template('home/home_page.html')

@app.route("/<token>")
def uploading_data(token):
    return "This is token"
