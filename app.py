#-*- coding:utf-8 -*-

from flask import Flask, jsonify, session, request, render_template, url_for, redirect
from items import GlobalMethod
from scripts import forms, helpers
import json, os

app = Flask(__name__)
app.secret_key = os.urandom(12)
app.debug = True

# @app.route('/', methods=['GET','POST'])
# def login():
#     if not session.get('logged_in') :
#         form = forms.LoginForm(request.form)
#         if request.method == 'POST' :
#             username = request.form['username'].lower()
#             password = request.form['password']
#             if form.validate():
#                 if helpers.credential_valid(username, password) :
#                     session['logged_in'] = True
#                     session['username'] = username
#                     return json.dumps({'status' : 'Login successful'})
#                 return json.dumps({'status' : 'Invalid user/pass'})
#             return json.dumps({'status' : 'Both fields required'})
#         return render_template('login.html', form = form)
#     user = helpers.get_user()
#     return render_template('home.html', user = user)
#
# @app.route('/signup', methods = ['GET', 'POST'])
# def signup():
#     if not session.get('logged_in') :
#     #     로그인 안했으면,
#         form = forms.LoginForm(request.form)
#         if request.method == 'POST' :
#             username = request.form['username'].lower()
#             password = helpers.hash_password(request.form['password'])
#             email = request.form['email']
#             if form.validate():
#                 if not helpers.username_taken(username) :
#                     helpers.add_user(username, password, email)
#                     session['logged_in'] = True
#                     session['username'] = username
#                     return json.dumps({'status' : 'Signup successful'})
#                 return json.dumps({'status': 'Username taken'})
#             return json.dumps({'status : User/Pass required'})
#         return render_template('login.html', form = form)
#     return redirect(url_for('login'))
#
# @app.route('/settings', methods = ['GET','POST'])
# def setting():
#     if session.get('logged_in') :
#         if request.method == 'POST' :
#             password = request.form['password']
#             if password != "" :
#                 password = helpers.hash_password(password)
#             email = request.form['email']
#             helpers.change_user(password=password, email = email)
#             return json.dumps({'status': 'Saved'})
#         user = helpers.get_user()
#         return render_template('settings.html', user=user)
#     return redirect(url_for('login'))
#
# @app.route("/logout")
# def logout():
#     session['logged_in'] = False
#     return redirect(url_for('login'))

@app.route('/api/')
def api_main():

    today = str(GlobalMethod.getToday())
    dDay = str(GlobalMethod.getDDay())
    thisTime = str(GlobalMethod.getthisTime())
    data = str(helpers.dbGetPredictedData(thisTime, 5))


    return jsonify(today=today, dDay = dDay, thisTime = thisTime
                   , data=data)

@app.route('/api/nums5')
def api_nums5():
    today = str(GlobalMethod.getToday())
    dDay = str(GlobalMethod.getDDay())
    thisTime = str(GlobalMethod.getthisTime())
    data = str(helpers.dbGetPredictedData(thisTime, 5))

    return jsonify(today=today, dDay=dDay, thisTime=thisTime
                   , data=data)
@app.route('/api/nums10')
def api_nums10():
    today = str(GlobalMethod.getToday())
    dDay = str(GlobalMethod.getDDay())
    thisTime = str(GlobalMethod.getthisTime())
    data = str(helpers.dbGetPredictedData(thisTime, 10))

    return jsonify(today=today, dDay=dDay, thisTime=thisTime
                   , data=data)

@app.route('/api/nums30')
def api_nums30():
    today = str(GlobalMethod.getToday())
    dDay = str(GlobalMethod.getDDay())
    thisTime = str(GlobalMethod.getthisTime())
    data = str(helpers.dbGetPredictedData(thisTime, 30))

    return jsonify(today=today, dDay=dDay, thisTime=thisTime
                   , data=data)

@app.route('/api/nums50')
def api_nums50():
    today = str(GlobalMethod.getToday())
    dDay = str(GlobalMethod.getDDay())
    thisTime = str(GlobalMethod.getthisTime())
    data = str(helpers.dbGetPredictedData(thisTime, 50))

    return jsonify(today=today, dDay=dDay, thisTime=thisTime
                   , data=data)


@app.route('/api/nums100')
def api_nums100():
    today = str(GlobalMethod.getToday())
    dDay = str(GlobalMethod.getDDay())
    thisTime = str(GlobalMethod.getthisTime())
    data = str(helpers.dbGetPredictedData(thisTime, 100))

    return jsonify(today=today, dDay=dDay, thisTime=thisTime
                   , data=data)

@app.route('/api/nums300')
def api_nums300():
    today = str(GlobalMethod.getToday())
    dDay = str(GlobalMethod.getDDay())
    thisTime = str(GlobalMethod.getthisTime())
    data = str(helpers.dbGetPredictedData(thisTime, 300))

    return jsonify(today=today, dDay=dDay, thisTime=thisTime
                   , data=data)


@app.route('/api/nums500')
def api_nums500():
    today = str(GlobalMethod.getToday())
    dDay = str(GlobalMethod.getDDay())
    thisTime = str(GlobalMethod.getthisTime())
    data = str(helpers.dbGetPredictedData(thisTime, 500))

    return jsonify(today=today, dDay=dDay, thisTime=thisTime
                   , data=data)


@app.route('/api/nums1000')
def api_numsAll():
    today = str(GlobalMethod.getToday())
    dDay = str(GlobalMethod.getDDay())
    thisTime = str(GlobalMethod.getthisTime())
    data = str(helpers.dbGetPredictedData(thisTime, 1000))

    return jsonify(today=today, dDay=dDay, thisTime=thisTime
                   , data=data)


app.run(host='0.0.0.0')