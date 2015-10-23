from flask import render_template, request, session, redirect, url_for
from app import app
import requests
import ast
import json


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    data = {'nickname': 'Zim', 'access_token': ''}
    if 'access_token' in session:
        data['access_token'] = session['access_token']
        return render_template('index.html', title='Home', user=data)
    else:
        return render_template('login.html')


@app.route('/auth')
def authorize():
    r = requests.get('https://www.formstack.com/api/v2/oauth2/authorize?client_id=12999&redirect_uri=http://formmap.herokuapp.com/token&response_type=code')
    return r.text

@app.route('/token')
def token():
    code = request.args.get('code')
    payload = {'client_id': 12999, 'client_secret': 'c3c4b56b4b', 'redirect_uri': 'http://formmap.herokuapp.com/token', 'grant_type': 'authorization_code', 'code': str(code)}
    r = requests.post('https://www.formstack.com/api/v2/oauth2/token', data=payload)
    r = json.loads(r.text)    
    session['access_token'] = r['access_token']
    return redirect(url_for('index'))
    
@app.route('/logout')
def logout():
    session.pop('access_token')
    return redirect(url_for('index'))
