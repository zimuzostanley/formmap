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
        headers = {'Authorization': 'Bearer ' + session['access_token']}
        r = requests.get('https://www.formstack.com/api/v2/form.json', headers=headers)
        forms = json.loads(r.text)
        print forms
        return render_template('index.html', data=data, forms=forms['forms'])
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

@app.route('/fields/<form_id>')
def fields(form_id):
    if 'access_token' in session:
        headers = {'Authorization': 'Bearer ' + session['access_token']}
        r = requests.get('https://www.formstack.com/api/v2/form/' + form_id + '/field.json', headers=headers)
        r = json.loads(r.text)
        fields = []
        for field in r:
            if field['type'] == 'select' or field['type'] == 'radio':
                fields.append(field)
        return render_template('fields.html', fields=fields)
    else:
        return render_template('login.html')

@app.route('/field/<field_id>')
def field(field_id):
    if 'access_token' in session:
        headers = {'Authorization': 'Bearer ' + session['access_token']}
        r = requests.get('https://www.formstack.com/api/v2/field/' + field_id + '.json', headers=headers)
        print r.text
        r = json.loads(r.text)
        options = []
        print r['options']
        for o in r['options']:
            pass
            #print o
            #options.append(r['options'][o])
            
        return render_template('map.html', options=options)
    else:
        return render_template('login.html')


