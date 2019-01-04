from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import learning2

import sqlite3
import importlib
import subprocess
import os
import json
from flask import Flask, render_template, request, jsonify,redirect, session
from learning2 import response
from prep_data import data_prepare
#import model2

# logger = logging.getLogger(__name__)
app = Flask(__name__)



def populate_dataset(user_input,reply,intent):
    conn = sqlite3.connect('./datasets/user_log.db')
    conn.execute('CREATE TABLE IF NOT EXISTS dataset (query TEXT,reply TEXT,intent TEXT)')
    c = conn.cursor()
    sqlscript = ('insert into dataset values (?,?,?);')
    if reply=="Sorry I did not understand.":
        c.execute(sqlscript, (user_input,"none","none"))
    else:
        c.execute(sqlscript,(user_input,reply,intent))
    conn.commit()
    return 1


# index
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index1.html')

@app.route('/get_message', methods=['POST'])
def get_message():
    message = request.form['message']
    return jsonify({'input': message})


@app.route('/get_bot', methods=['POST'])
def activatebot():

    try:
        data = request.get_json(force=True)
        message,intent,possible_query= start_bot(data.get('message'))
        print("iam message",data.get('message'))
        populate_dataset(data.get('message'),message,intent)
        tags=possible_query
        msg=""
        return jsonify({'status':True,'message':message, 'msg':msg})
    except:
        data = request.form['message']
        print(data)
        message, intent,possible_query = start_bot(data)
        status = True
        tags=possible_query
        msg = "Retrived successfully."
        print(msg)
        print(data,message,intent)
        populate_dataset(data, message, intent)
        return jsonify({'status': status, 'body': message, 'msg': msg,'tags':tags})


@app.route('/train_board', methods = ['POST', 'GET'])
def sql_database():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        from functions.sqlquery import sql_query
        results = sql_query(''' SELECT * FROM dataset''')
        msg = 'SELECT * FROM dataset'
        return render_template('t_board.html', results=results, msg=msg)

@app.route('/login', methods=['POST', 'GET'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
        failed_msg = "Username or Password didn't match."
        return sql_database()

    else:
       
        return render_template('login.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()

@app.route('/insert',methods = ['POST', 'GET']) #this is when user submits an insert
def sql_datainsert():
    from functions.sqlquery import sql_edit_insert, sql_query
    if request.method == 'POST':
        reply = request.form['reply']
        query = request.form['query']
        intent = request.form['intent']
        sql_edit_insert(''' INSERT INTO dataset (query,reply,intent) VALUES (?,?,?) ''', (query,reply,intent) )
    results = sql_query(''' SELECT * FROM dataset''')
    msg = 'INSERT INTO dataset (query,reply,intent) VALUES ('+query+','+reply+','+intent+')'
    return render_template('t_board.html', results=results, msg=msg)

@app.route('/train_board/delete',methods = ['POST', 'GET']) #this is when user clicks delete link
def sql_datadelete():
    from functions.sqlquery import sql_delete, sql_query
    if request.method == 'GET':
        lreply = request.args.get('lreply')
        fquery = request.args.get('fquery')
        sql_delete(''' DELETE FROM dataset where query = ? and reply = ?''', (fquery,lreply) )
    results = sql_query(''' SELECT * FROM dataset''')
    msg = 'DELETE FROM dataset WHERE query = ' + fquery + ' and reply = ' + lreply
    return render_template('t_board.html', results=results, msg=msg)

@app.route('/train_board/query_edit',methods = ['POST', 'GET']) #this is when user clicks edit link
def sql_editlink():
    from functions.sqlquery import sql_query, sql_query2
    if request.method == 'GET':
        elreply = request.args.get('elreply')
        efquery = request.args.get('efquery')
        eresults = sql_query2(''' SELECT * FROM dataset where query = ? and reply = ?''', (efquery,elreply))
    results = sql_query(''' SELECT * FROM dataset''')
    return render_template('t_board.html', eresults=eresults, results=results)

@app.route('/train_board/edit',methods = ['POST', 'GET']) #this is when user submits an edit
def sql_dataedit():
    from functions.sqlquery import sql_edit_insert, sql_query
    if request.method == 'POST':
        old_reply = request.form['old_reply']
        old_query = request.form['old_query']
        reply = request.form['reply']
        query = request.form['query']
        intent = request.form['intent']
        sql_edit_insert(''' UPDATE dataset set query=?,reply=?,intent=? WHERE query=? and reply=? ''', (query,reply,intent,old_query,old_reply) )
    results = sql_query(''' SELECT * FROM dataset''')
    msg = 'UPDATE dataset set query = ' + query + ', reply = ' + reply + ', intent = ' + intent + '  WHERE query = ' + old_query + ' and reply = ' + old_reply
    return render_template('t_board.html', results=results, msg=msg)

@app.route('/train_board/prepare_data',methods=['POST','GET'])#for data preparation from sql to json
def prepare_data():
    data_prepare()
    return redirect('/train_board/complete_preparation')

@app.route('/train_board/complete_preparation',methods=['POST','GET'])
def complete_preparation():
    return render_template('training.html')

@app.route('/train_board/train_data',methods=['GET'])
def train_model():
    print("iam in")
    subprocess.check_call(["python3", "./model2.py"])
    reply = "<strong>Training in progress...</strong>"
    print(reply)
    #modelreload
    importlib.reload(learning2)
    return redirect('/')


    
def start_bot(message):

    reply,intent,possible_query=response(message)
    print("iam the possible query",possible_query)
    return reply, intent, possible_query





if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=5000, debug=True)
    #train_dialogue()
    #run_weather_bot()e