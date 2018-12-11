from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

import sys
import os
from flask import Flask, render_template, jsonify, flash, redirect, url_for, session, logging, request, jsonify

from learning2 import response

# logger = logging.getLogger(__name__)
app = Flask(__name__)

# index
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/get_message', methods=['POST'])
def get_message():
    message = request.form['message']
    return jsonify({'input': message})


@app.route('/get_bot', methods=['POST'])
def activatebot():
    # data = request.get_json(force=True)
    data = request.form['message']
    # message = start_bot(data.get('message'))
    message = start_bot(data)
    # status = True
    # msg = "Retrived successfully."

    return jsonify({'status': status, 'body': message, 'msg':msg})



def start_bot(message):
	reply=str(response(message))
	return reply

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
	#train_dialogue()
	#run_weather_bot()