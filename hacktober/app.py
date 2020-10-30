from flask import Flask, request, redirect, url_for, render_template, session, send_from_directory, send_file, flash, abort, make_response
from werkzeug.utils import secure_filename
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_details.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
	""" Create user table"""
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(5000), unique=False)
	language = db.Column(db.String(100), unique=False)
	subject = db.Column(db.String(100), unique=False)
	location = db.Column(db.String(100), unique=False)

	def __init__(self, username, password, language, subject, location):
		self.username = username
		self.password = password
		self.language = language
		self.subject = subject
		self.location = location

@app.route('/register')
def call_page_register_user():
	return render_template('register.html')
@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/home')
def back_home():
	return render_template('index.html')

@app.route('/')
def index():
	return render_template('index.html')
	
@app.route('/tutor')
def tutor():
	return render_template('tutors.html')

@app.route('/mypage')
def mypage():
	return render_template('mypage.html')



@app.route('/main')
def index_after_login():
	if not session.get('logged_in'):
		return render_template('index.html')
	return render_template('home_dup.html',Name = session['username'])

@app.route('/register-new-user', methods = ['GET', 'POST'])
def register_user():
	try:
		if request.method == 'POST':
			new_user = User(
				username = request.form['username'],
				password = encrypt(request.form['password'],
				language = request.form['language'],
				subject = request.form['subject'],
				location = request.form['location'],
				))
			db.session.add(new_user)
			db.session.commit()
			session['logged_in'] = True
			session['username'] = request.form['username']
			return render_template('home_dup.html')
	except:
		return render_template('register.html', Sentence="Username aldready exists, try a different name!!!")

@app.route('/after-login', methods = ['POST'])
def after_login():
    try:
        if request.method == 'POST':
            name = request.form['username']	
            password_entered = request.form['password']
            result = User.query.filter_by(username=name).first()
            password = result.password
            if result is not None:
                session['logged_in'] = True
                session['username'] = name
                if password == encrypt(password_entered):
                    return redirect(url_for('index_after_login'))
                return render_template('login.html', Sentence="Wrong password")
            return render_template('register.html', Sentence="Please Register First")
    except:
        return render_template('register.html',Sentence="Oops!! Give us a moment!!")	

@app.route("/logout")
def logout():
	"""Logout Form"""
	session['logged_in'] = False
	return render_template('index.html')

def encrypt(text): 
    result = "" 
    s = 1
    for char in text: 
        if (char.isupper()): 
            result += chr((ord(char) + s-65) % 26 + 65)  
        else: 
            result += chr((ord(char) + s - 97) % 26 + 97)
    return convert(result) 
def convert(result):
    result1 = ""
    for i in result[:len(result) // 2]:
        #print(i,end = " ")
        i = hex(ord(i))
        result1 += i
    for i in result[len(result) // 2:]:
        #print(i,end = " ")
        i = bin(ord(i))
        result1 += i
    return result1
if __name__ == '__main__':
	#app.run(host="0.0.0.0", port=80)
	app.secret_key = 'secret'
	app.debug = True
	db.create_all()
	app.run()

