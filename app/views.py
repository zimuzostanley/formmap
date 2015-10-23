from flask import render_template, request
from app import app
import requests

@app.route('/')
@app.route('/index')
def index():
    access_token = request.args.get('access_token')
    user_id = request.args.get('user_id')
    expires_in = request.args.get('expires_in')
    if access_token:
        return access_token + "\t" + user_id + "\t" + expires_in

    
    user = {'nickname': 'Zim'}
    return render_template('index.html', title='Home',user=user)


@app.route('/auth')
def authorize():
    r = requests.get('https://www.formstack.com/api/v2/oauth2/authorize?client_id=12999&redirect_uri=http%3A%2F%2Fformmap.herokuapp.com%2Ftoken&response_type=code')
    return r.text

@app.route('/token')
def token():
    code = request.args.get('code')
    r = requests.get('https://www.formstack.com/api/v2/oauth2/authorize?client_id=12999&client_secret=c3c4b56b4b&redirect_uri=http%3A%2F%2Fformmap.herokuapp.com&grant_type=authorization_code&code=' + code)
    return "Authorized"
