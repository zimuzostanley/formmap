from flask import render_template, request, session, redirect, url_for, jsonify
from app import app
import requests
import ast
import json


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    data = {'nickname': 'Zim', 'access_token': ''}
    if 'access_token' in session:
        headers = {'Authorization': 'Bearer ' + session['access_token']}
        r = requests.get('https://www.formstack.com/api/v2/form.json', headers=headers)
        forms = json.loads(r.text)
        return render_template('map.html', forms=forms['forms'])
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
        
        return jsonify(**{'fields': fields})
    else:
        return render_template('login.html')

@app.route('/field/<form_id>/<field_id>')
def field(form_id, field_id):
    if 'access_token' in session:
        headers = {'Authorization': 'Bearer ' + session['access_token']}
        r = requests.get('https://www.formstack.com/api/v2/form/' + form_id + '/field.json', headers=headers)
        r = json.loads(r.text)
        options = []
        submissions = {}
        for field in r:
            if field['id'] == field_id:
                options = field['options']
                break
        for option in options:
            submissions[option['value']] = {'label': option['label'], 'value': option['value'], 'color': 'B1CFFE', 'data': []}

        r = requests.get('https://www.formstack.com/api/v2/form/' + form_id + '/submission.json', headers=headers)
        r = json.loads(r.text)

        r = r['submissions']
        for submission in r:
            if submission.get('longitude') and submission.get('latitude'):
                q = requests.get('https://www.formstack.com/api/v2/submission/' + submission['id'] + '.json', headers=headers)
                q = json.loads(q.text)
                for d in q['data']:
                    if d['field'] == field_id:
                        submissions[d['value']]['data'].append({'id': submission['id'], 'lon': submission['longitude'], \
                                                                'lat': submission['latitude']})
                        break
        _submissions = []
        for key, value in submissions.iteritems():
            _submissions.append(value)
        return jsonify(**{'options': options, 'submissions': submissions})
    else:
        return render_template('login.html')

