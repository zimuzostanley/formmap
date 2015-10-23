from flask import render_template, request
from app import app
import requests
import json

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    user = {'nickname': 'Zim'}
    return render_template('index.html', title='Home',user=user)


@app.route('/auth')
def authorize():
    r = requests.get('https://www.formstack.com/api/v2/oauth2/authorize?client_id=12999&redirect_uri=http%3A%2F%2Fformmap.herokuapp.com%2Ftoken&response_type=code')
    return r.text

@app.route('/token')
def token():
    code = request.args.get('code')
    payload = {'client_id': 12999, 'client_secret': 'c3c4b56b4b', 'redirect_uri': 'http%3A%2F%2Fformmap.herokuapp.com%2Ftoken%2F', 'grant_type': 'authorization_code', 'code': str(code)}
    r = requests.post('https://www.formstack.com/api/v2/oauth2/token', data=json.dumps(payload))
    print payload
    print "Payload"
    return r.text
    
