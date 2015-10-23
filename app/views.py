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
    r = requests.get('https://www.formstack.com/api/v2/oauth2/authorize?client_id=12999&redirect_uri=http%3A%2F%2Fformmap.herokuapp.com%2Ftoken&response_type=code')
    return r.text

@app.route('/token')
def token():
    code = request.args.get('code')
    r = requests.post('https://www.formstack.com/api/v2/oauth2/token', data={'client_id': '12999', 'redirect_uri': 'http%3A%2F%2Fformmap.herokuapp.com%2Ftoken', 'grant_type': 'authorization_code', 'code': code})
    return code + "\t" + r.text
    
