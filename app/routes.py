from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Stephen'}
    posts = [
        {
            'author': { 'username': 'Stephen'},
            'body': 'I am a software engineer!'
        },
        {
            'author': { 'username': 'Victor'},
            'body': 'I am a data scientist!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts = posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')