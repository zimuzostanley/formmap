from flask import render_template, request
from app import app
import requests


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    user = {'nickname': 'Zim'}
    return render_template('index.html', title='Home',user=user)


@app.route('/auth')
def authorize():
    r = requests.get('https://www.formstack.com/api/v2/oauth2/authorize?client_id=12999&redirect_uri=http://formmap.herokuapp.com/token&response_type=code')
    return r.text

@app.route('/token')
def token():
    code = request.args.get('code')
    payload = {'client_id': 12999, 'client_secret': 'c3c4b56b4b', 'redirect_uri': 'http://formmap.herokuapp.com/token', 'grant_type': 'authorization_code', 'code': str(code)}
    r = requests.post('https://www.formstack.com/api/v2/oauth2/token', data=payload)
    print payload
    print "Payload"
    return r.text
    
