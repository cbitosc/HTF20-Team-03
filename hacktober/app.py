from flask import Flask, request, redirect, url_for, render_template, session, send_from_directory, send_file, flash, abort, make_response
from werkzeug.utils import secure_filename
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///latest.db'
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
	email = db.Column(db.String(100), unique=True)
	pno = db.Column(db.String(100), unique=True)

	def __init__(self, username, password, language, subject, location, email, pno):
		self.username = username
		self.password = password
		self.language = language
		self.subject = subject
		self.location = location
		self.email = email
		self.pno = pno

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
	user = session['username']
	result = User.query.filter_by(username=user).first()
	lang = result.language
	sub = result.subject
	loc = result.location
	mail = result.email
	pno = result.pno
	return render_template('mypage.html', user = user, lang = lang, sub = sub, loc = loc, mail = mail, pno = pno )



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
				password = encrypt(request.form['password']),
				language = request.form['language'],
				subject = request.form['subject'],
				location = request.form['location'],
				email = request.form['email'],
				pno = request.form['pno']
				)
			db.session.add(new_user)
			db.session.commit()
			session['logged_in'] = True
			session['username'] = request.form['username']
			return render_template('home_dup.html')
	except:
		return render_template('register.html', Sentence="Credentials already exists, try a different name!")

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

'''@app.route('/after-search', methods = ['POST'])
def after_search():
		if request.method == 'POST':
			name = request.form['Name']	
			languages = request.form['languages']
			subject = request.form['Subjects']
			location = request.form['Location']	
			result = User.query.filter_by(location=location).all()
			print(result)
			l = []
			for i in result:
				l.append(i.username)
			return render_template('dummy.html', item=result)'''
			#return render_template('dummy.html')

@app.route('/search-tutor', methods = ['POST'])
def search_tutor():
	try:
		if request.method == 'POST':
			name = request.form['Name']		
			result = User.query.filter_by(username=name).all()
			print(type(result))
			un = []
			loc = []
			sub = []
			lang = []
			d = dict()
			for index, i in enumerate(result):
				d[index] = [i.username] + [i.location] + [i.subject] + [i.language] + [i.email] + [i.pno]
			print(d)
			return render_template('dummy.html', name=d.values())
	except:
			return render_template("error.html")

@app.route('/search-subject', methods = ['POST'])
def search_sub():
	try:
		if request.method == 'POST':
			subject = request.form['Subjects']	
			result = User.query.filter_by(subject=subject).all()
			print(result)
			d = dict()
			for index, i in enumerate(result):
				d[index] = [i.username] + [i.location] + [i.subject] + [i.language] + [i.email] + [i.pno]
			return render_template('dummy.html', name=d.values())
	except:
			return render_template("error.html")
@app.route('/search-location', methods = ['POST'])
def search_loc():
	try:
		if request.method == 'POST':
			location = request.form['Location']	
			result = User.query.filter_by(location= location).all()
			print(result)
			d = dict()
			for index, i in enumerate(result):
				d[index] = [i.username] + [i.location] + [i.subject] + [i.language] + [i.email] + [i.pno]
			print(d)
			return render_template('dummy.html', name=d.values())
	except:
			return render_template("error.html")

@app.route('/search-language', methods = ['POST'])
def search_lang():
	try:
		if request.method == 'POST':
			languages = request.form['languages']	
			result = User.query.filter_by(language = languages).all()
			print(result)
			d = dict()
			for index, i in enumerate(result):
				d[index] = [i.username] + [i.location] + [i.subject] + [i.language] + [i.email] + [i.pno]
			print(d)
			return render_template('dummy.html', name=d.values())
	except:
		return render_template("error.html")
	

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

