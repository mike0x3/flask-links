from flask import Flask, render_template, url_for, request, redirect, flash, abort, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import threading
import json
import generator
import os
from os.path import join, dirname, realpath
import smtplib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cards.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Fh6dkd3sg3Bh28Gfnh4D'
db = SQLAlchemy(app)
UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/images/')
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH
app.config['MAX_CONTENT_PATH'] = 1024 * 1024

index_html = 'index.html'
contattaci_html = 'contattaci.html'

class Cards(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50), nullable=True)
	text = db.Column(db.Text, nullable=True)
	image_link = db.Column(db.Text, nullable=True)

	def __repr__(self):
		return f'<cards {self.id}>'

class Flash(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50), nullable=True)
	text = db.Column(db.Text, nullable=True)
	style = db.Column(db.String(10), nullable=True)

	def __repr__(self):
		return f'<flash {self.id}>'

#print(Cards.query.filter_by(id=1).first().title)

@app.route('/', methods=["GET"])
def home():
	codes_list = []
	card1 = Cards.query.filter_by(id=1).first()
	card2 = Cards.query.filter_by(id=2).first()
	card3 = Cards.query.filter_by(id=3).first()
	flash_mex = Flash.query.filter_by(id=1).first()
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
		return render_template(index_html, codes=codes_list, all_codes=codes_list_backup, random_num=random_num, link=link, code=code, card1=card1, card2=card2, card3=card3, flash_mex=flash_mex)
	else:
		return render_template(index_html, codes=codes_list, all_codes=codes_list_backup, random_num=random_num, card1=card1, card2=card2, card3=card3, flash_mex=flash_mex)

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
			
			card1 = Cards.query.filter_by(id=1).first()
			card2 = Cards.query.filter_by(id=2).first()
			card3 = Cards.query.filter_by(id=3).first()
			flash('Tasto attivato')
			return render_template('dev.html', card1=card1, card2=card2, card3=card3)
	except Exception as e:
		pass

	if request.method == 'POST':
		try:
			if request.form['psw'] == "Laougay69":
				session['admin'] = True
				flash('Tasto attivato')
				card1 = Cards.query.filter_by(id=1).first()
				card2 = Cards.query.filter_by(id=2).first()
				card3 = Cards.query.filter_by(id=3).first()

				return render_template('dev.html', card1=card1, card2=card2, card3=card3)
			else:
				flash('Codice errato')
				return render_template('dev.html')
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

@app.route('/db', methods=['POST', 'GET'])
def add_to_db():
	if request.method == "POST":
		if "title1" in request.form:
			title = request.form['title1']
			text = request.form['text1']
			image_link = request.form['image_link1']
			upd_data = Cards.query.filter_by(id=1).first()
			upd_data.title = title
			upd_data.text = text
			upd_data.image_link = image_link
			db.session.commit()
			flash('Informazioni in card modificate con successo')
			return redirect('/dev')

		if "title2" in request.form:
			title = request.form['title2']
			text = request.form['text2']
			image_link = request.form['image_link2']
			upd_data = Cards.query.filter_by(id=2).first()
			upd_data.title = title
			upd_data.text = text
			upd_data.image_link = image_link
			db.session.commit()
			flash('Informazioni in card modificate con successo')
			return redirect('/dev')

		if "title3" in request.form:
			title = request.form['title3']
			text = request.form['text3']
			image_link = request.form['image_link3']
			upd_data = Cards.query.filter_by(id=3).first()
			upd_data.title = title
			upd_data.text = text
			upd_data.image_link = image_link
			db.session.commit()
			flash('Informazioni in card modificate con successo')
			return redirect('/dev')

		if 'file' in request.files:
			file = request.files['file']
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
			flash('Immagine salvata con successo')
			return redirect('/dev')

		if 'flash_text' in request.form:
			radio = request.form['option']
			testo = request.form['flash_text']
			titolo = request.form['flash_title']

			if radio == "danger":
				flash1 = Flash.query.filter_by(id=1).first()
				flash1.title = titolo
				flash1.text = testo
				flash1.style = "danger"
				db.session.commit()
				flash('Testo aggiunto al sito!')
				return redirect('/dev')

			if radio == "ok":
				flash1 = Flash.query.filter_by(id=1).first()
				flash1.title = titolo
				flash1.text = testo
				flash1.style = "ok"
				db.session.commit()
				flash('Testo aggiunto al sito!')
				return redirect('/dev')

			if radio == "new":
				flash1 = Flash.query.filter_by(id=1).first()
				flash1.title = titolo
				flash1.text = testo
				flash1.style = "new"
				db.session.commit()
				flash('Testo aggiunto al sito!')
				return redirect('/dev')

			if radio == "rimuovi":
				flash1 = Flash.query.filter_by(id=1).first()
				flash1.title = ""
				flash1.text = ""
				flash1.style = ""
				db.session.commit()
				flash('Testo rimosso  dal sito con successo!')
				return redirect('/dev')

@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html'), 404
