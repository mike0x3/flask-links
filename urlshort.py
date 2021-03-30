from flask import Flask, render_template, url_for, request, redirect, flash, abort, session
from flask_sqlalchemy import SQLAlchemy
import threading
import json
import generator
import os.path
import smtplib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cards.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Fh6dkd3sg3Bh28Gfnh4D'
db = SQLAlchemy(app)

index_html = 'index.html'
contattaci_html = 'contattaci.html'

class Cards(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50), nullable=True)
	text = db.Column(db.Text, nullable=True)
	image_link = db.Column(db.Text, nullable=True)

	def __repr__(self):
		return f'<cards {self.id}>'

@app.route('/', methods=["GET"])
def home():
	codes_list = []
	for code in session.keys():
		codes_list.append(code)
	codes_list_backup = codes_list.copy()
	if len(codes_list) >= 6:
		del codes_list[5:]
		codes_list.append("Vedi tutto")
	else:
		pass
	random_num = generator.get_num()
	if request.method == "GET":
		link = request.values.get('link')
		code = request.values.get('code')
		return render_template(index_html, codes=codes_list, all_codes=codes_list_backup, random_num=random_num, link=link, code=code)
	else:
		return render_template(index_html, codes=codes_list, all_codes=codes_list_backup, random_num=random_num)

@app.route('/contattaci', methods=["POST", "GET"])
def contattaci():
	if request.method == "POST":
		nome = request.form['name']
		email = request.form['email']
		message = request.form['text']
		sender_email = "mrchela123@gmail.com"
		receiver_email = "telegiver1@gmail.com"
		sender_password = "Asokina76"
		email_text = f"""\
		Subject: Richiesta da URL Shorter

		E arrivata una richiesta da parte di\n
		Nome Cognome: {nome}\n 
		Email: {email}\n
		Testo del messaggio: {message}"""
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(sender_email, sender_password)
		server.sendmail(sender_email, receiver_email, email_text)
		flash('La sua domanda é stata inviata ai nostri admin!')
	return render_template(contattaci_html)

@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
	if request.method == 'POST':
		urls={}
		codes_list = []
		for code in session.keys():
			codes_list.append(code)
		codes_list_backup = codes_list.copy()
		if len(codes_list) >= 6:
			del codes_list[5:]
			codes_list.append("Vedi tutto")
		else:
			pass
		random_num = generator.get_num()
		if os.path.exists('urls.json'):
			with open('urls.json') as urls_file:
				urls = json.load(urls_file)
		if request.form['code'] in urls.keys():
			flash('Questo nome é gia stato preso, scegline un altro!')
			return redirect(url_for('home'))
		if request.form['code'] == '_flashes':
			flash("Prova un altro nome")
			return render_template('index.html', codes=codes_list, all_codes=codes_list_backup, random_num=random_num)

		urls[request.form['code']] = {'url':request.form['url']}

		with open('urls.json', 'w') as url_file:
			json.dump(urls, url_file) 
			session[request.form['code']] = True
		flash('Link aggiunto')
		return redirect(url_for('home', code=request.form['code'], link=request.form['url']))
	else:
		return redirect(url_for('home'))

@app.route('/<string:code>')
def redirect_to_url(code):
	if os.path.exists('urls.json'):
		with open('urls.json') as urls_file:
			urls = json.load(urls_file)
			if code in urls.keys():
				if 'url' in urls[code].keys():
					return redirect(urls[code]['url'])

	return abort(404)

@app.route('/login')
def login():
	return '<h1>Attualmente in sviluppo</h1><p>Nella versione BETA 3.0 sara disponibile solo per gli admin</p><p><a href="/">Torna alla home</a></p>'

@app.route('/dev', methods=['GET', 'POST'])
def dev():
	global index_html
	global contattaci_html
	try:
		if session['admin'] == True:
			try:
				if request.form['deactiv'] == 'Disattiva Lavori in Corso':
					index_html = "index.html"
					contattaci_html = "contattaci.html"

			except Exception as e:
				pass

			try:
				if request.form['activ'] == 'Attiva Lavori in Corso':			
					index_html = "work_in_progress.html"
					contattaci_html = "work_in_progress.html"
			except Exception as e:
				pass

			try:
				if request.form['Logout'] == "Logout":
					session.pop('admin')
					return render_template("dev.html")
			except Exception as e:
				pass
			flash('Tasto attivato')
			return render_template('dev.html')
	except Exception as e:
		pass

	if request.method == 'POST':
		try:
			if request.form['psw'] == "Laougay69":
				session['admin'] = True
				flash('Tasto attivato')
			else:
				flash('Codice errato')
		except Exception as e:
			pass
		try:
			if request.form['deactiv'] == 'Disattiva Lavori in Corso':
				index_html = "index.html"
				contattaci_html = "contattaci.html"

		except Exception as e:
			pass

		try:
			if request.form['activ'] == 'Attiva Lavori in Corso':			
				index_html = "work_in_progress.html"
				contattaci_html = "work_in_progress.html"
		except Exception as e:
			pass

		try:
			if request.form['Logout'] == "Logout":
				session.pop('admin')
				return render_template("dev.html")
		except Exception as e:
			pass

	return render_template('dev.html')

@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html'), 404
