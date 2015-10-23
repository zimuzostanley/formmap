from flask import render_template, request
from app import app
import requests

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Zim'}
    
    return render_template('index.html', title='Home',user=user)


@app.route('/auth')
def authorize():
    r = requests.get('https://www.formstack.com/api/v2/oauth2/authorize?client_id=12999&redirect_uri=formmap.herokuapp.com/token&response_type=code')
    return r.text

def token():
    code = request.args.get('code')
    return code
