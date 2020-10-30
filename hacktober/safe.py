import os
import os.path
from flask import Flask, request, redirect, url_for, render_template, session, send_from_directory, send_file
from werkzeug.utils import secure_filename
#import DH
import pickle
import random

UPLOAD_FOLDER = './media/text-files/'
UPLOAD_KEY = './media/public-keys/'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

'''
-----------------------------------------------------------
					PAGE REDIRECTS
-----------------------------------------------------------
'''
@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/home')
def back_home():
	return render_template('index.html')

@app.route('/')
def index():
	return render_template('index.html')

if __name__ == "__main__":
  app.run()
