# -*- coding: utf8 -*- 
import pymysql, os, random, urllib.request

#from flask.ext.login import UserMixin

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db 
from app.forms import LoginForm, SearchForm,RegistrationForm, AddfilmsForm
from app.models import User, Add_films

from collections import namedtuple
from itertools import groupby

from werkzeug.urls import url_parse

picFolder = os.path.join('static','pics')
app.config['UPLOAD_FOLDER'] = picFolder 

#Message = namedtuple('Message', 'text tag')
#results = []
global kek
#movies = []
#actors=[]
#text_films=[]
#messages=[]
#Actors=namedtuple('Actors', 'actor')
#actors=[]
global added
added = []
connection = pymysql.connect(host='localhost', user='root', password='newpassword', db='kek')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		print(form.password.data)
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))

		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('search')
		return redirect(next_page)
		#return redirect(url_for('index'))
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#@app.route('/')
@app.route('/index')
@login_required 
def index():
    user = {'username': 'Я'}
    return render_template('index.html', title='Home Page', user=user)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('You are now a registered user!')
		return redirect(url_for('login'))
	return render_template('registration.html', title='Register', form=form)

@app.route("/search_results", methods=('GET', 'POST')) 
@login_required
def search_results():
	form = SearchForm()
	user = {'user':"user1"}
	return render_template('search_results.html',user=user,form=form)

def sql_request_search(form_search1, form_search2):
	cursor2=connection.cursor()
	sql_request = "SELECT movie FROM table_name WHERE "
	if form_search1 != 'none' and form_search2 == 'none':
		sql2 =  sql_request+ "year LIKE " + "'%" + form_search1 + "%'" 

	elif form_search1 == 'none' and form_search2 != 'none':
		sql2 =  sql_request+ "rating_ball LIKE " + "'%" + form_search2 + "%'"	

	elif form_search1 != 'none' and form_search2 != 'none':
		sql2 =  sql_request+ "rating_ball LIKE " + "'%" + form_search2 + "%'" + "AND " + "year LIKE " + "'%" + form_search1 + "%'" 
	cursor2.execute(sql2)
	results2=cursor2.fetchall()
	return(results2)
	
@app.route('/myfilms', methods=['GET','POST'])
@login_required
def myfilms():
	masfilms=[]
	form = AddfilmsForm()
	user= User.query.filter_by(username=current_user.id).first_or_404()
	#print('отладка ',form.validate_on_submit() ,form.errors.items())
	if request.method == "POST":
		if form.validate_on_submit():
			film= form.film.data
			print(film)
			#posts= [
			#	{'author' : user, 'films' : film}
			#	]
			f = Add_films(films=film, author=user)
			db.session.add(f)
			db.session.commit()
			r=Add_films.query.all()
			cursor=connection.cursor()
			sql= "SELECT movie FROM table_name"
			cursor.execute(sql)
			results=cursor.fetchall()
		
			mas=['Побег из Шоушенка', 'Зеленая миля', 'Форрест Гамп', 'Список Шиндлера', '1+1', 'Начало', 'Леон', 'Король Лев', 'Бойцовский клуб', 'Иван Васильевич меняет профессию', 'Жизнь прекрасна', 'Достучаться до небес', 'Крестный отец', 'Криминальное чтиво', 'Операция «Ы» и другие приключения Шурика', 'Престиж', 'Игры разума', 'Интерстеллар', 'Властелин колец: Возвращение Короля', 'Гладиатор', 'Назад в будущее', 'Карты; деньги; два ствола', 'Матрица', 'Бриллиантовая рука', 'Отступники', 'Поймай меня; если сможешь', 'Пианист', 'Властелин колец: Братство кольца', 'В бой идут одни «старики', 'ВАЛЛ·И', 'Тайна Коко', 'Большой куш', 'Властелин колец: Две крепости', 'Американская история\xa0X', 'Джентльмены удачи', 'Пираты Карибского моря: Проклятие Черной жемчужины', 'Остров проклятых', 'Темный рыцарь', 'Пролетая над гнездом кукушки', 'Титаник', '12 разгневанных мужчин', 'Запах женщины', 'Пробуждение', 'В джазе только девушки', 'Хатико: Самый верный друг', 'Огни большого города', 'Унесённые призраками', 'Кавказская пленница; или Новые приключения Шурика', '...А зори здесь тихие', 'Эта замечательная жизнь', 'Хороший; плохой; злой', 'Хористы', 'Приключения Шерлока Холмса и доктора Ватсона: Собака Баскервилей', 'Семь', 'Молчание ягнят', 'Как приручить дракона', 'Шоу Трумана', 'Терминатор 2: Судный день', 'Джанго освобожденный', 'Крестный отец\xa02', 'Клаус', 'Собачье сердце', 'Нокдаун', 'Игра', 'Храброе сердце', 'Шерлок Холмс и доктор Ватсон: Знакомство', 'Москва слезам не верит', 'Джентльмены', 'Гран Торино', 'Одержимость', 'Прислуга', 'Человек дождя', 'Изгой', 'Летят журавли', 'Шестое чувство', 'Зверополис', 'Офицеры', 'Спасти рядового Райана', 'Малыш', 'Эффект бабочки', 'В погоне за счастьем', 'Белый Бим Черное ухо', 'Судьба человека', 'Красавица и чудовище', 'Назад в будущее\xa02', 'Дневник памяти', 'Укрощение строптивого', 'Однажды в Америке', 'Римские каникулы', 'Унесенные ветром', 'Служебный роман', 'Балто', 'Темный рыцарь: Возрождение легенды', 'Жизнь других', 'Счастливое число Слевина', 'Адвокат дьявола', 'Амадей', 'Зеленая книга', '…А в душе я танцую', 'Они сражались за Родину', 'Шерлок Холмс и доктор Ватсон: Смертельная схватка', 'Ходячий замок', 'Гонка', 'Брат', 'Баллада о солдате', 'Малышка на миллион', 'Хоббит: Нежданное путешествие', 'Девчата', 'Свидетель обвинения', 'Шерлок Холмс и доктор Ватсон: Кровавая надпись', 'Мальчик в полосатой пижаме', 'Общество мертвых поэтов', 'Пятый элемент', 'Одиннадцать друзей Оушена', 'Один дома', 'День сурка', 'Казино', 'Артист', 'Приключения Шерлока Холмса и доктора Ватсона: Охота на тигра', 'Аладдин', 'Добро пожаловать; или Посторонним вход воспрещен', 'Новые времена', 'Могила светлячков', 'Невидимая сторона', 'Город Бога', 'Любовь и голуби', 'Как украсть миллион', 'Семь жизней', 'Шерлок Холмс и доктор Ватсон: Король шантажа', 'Легенда о пианисте', 'Меня зовут Кхан', 'Афера', 'Привидение', 'Танцующий с волками', '12 стульев', 'Жизнь Дэвида Гейла', 'Рэй', 'Шерлок Холмс и доктор Ватсон: Сокровища Агры', 'Терминал', 'Самый быстрый Indian', 'Назад в будущее\xa03', 'Умница Уилл Хантинг', 'Славные парни', 'Пираты Карибского моря: Сундук мертвеца', 'Лицо со шрамом', 'На несколько долларов больше', 'Ледниковый период', 'Головоломка', 'Король говорит!', 'Блеф', 'Ромео и Джульетта', 'Перед классом', 'Планета Ка-Пэкс', 'Золотой теленок', 'Шерлок Холмс', 'Амели', 'Семь самураев', 'В случае убийства набирайте «М»', 'Нюрнбергский процесс', 'Бешеные псы', 'Заплати другому', 'Корпорация монстров', 'Вам и не снилось...', 'Вечное сияние чистого разума', 'Три билборда на границе Эббинга; Миссури', 'Ганди', 'Апокалипсис сегодня', 'Воин', 'Тот самый Мюнхгаузен', 'Белый плен', 'Андрей Рублев', 'Отец солдата', 'Звёздные войны: Эпизод 3 – Месть Ситхов', 'Тренер Картер', 'Красота по-американски', 'Писатели свободы', 'Мой сосед Тоторо', 'Твоё имя', 'Человек-слон', 'Исчезнувшая', 'Индиана Джонс и последний крестовый поход', 'Схватка', 'Военный ныряльщик', 'Октябрьское небо', 'Принцесса Мононоке', 'Знахарь', 'Джокер', 'Звёздные войны: Эпизод 6 – Возвращение Джедая', 'Психо', 'Ип Ман', 'Новый кинотеатр «Парадизо»', 'Шрэк', 'Иллюзионист', 'Последний самурай', 'Звёздочки на земле', 'Гарри Поттер и узник Азкабана', 'Легенда №17', 'Берегись автомобиля', 'Ирония судьбы; или С легким паром!', 'Брат\xa02', 'Трасса 60', 'Цирк', 'Жестокий романс', 'Загадочная история Бенджамина Баттона', 'Хоббит: Пустошь Смауга', 'Пока не сыграл в ящик', 'Хулиганы', 'Тэмпл Грандин', 'Гарри Поттер и философский камень', 'Ford против Ferrari', 'Дурак', 'Я – Сэм', 'Гарри Поттер и Дары Смерти: Часть II', 'Апокалипсис', 'Подмена', 'Рататуй', 'Песнь моря', 'Ураган', 'Медведь', 'Крепкий орешек', 'Три идиота', 'Золотая лихорадка', 'Убить пересмешника', 'Аватар', 'Крупная рыба', 'Столкновение', 'Завтра была война', 'Звёздные войны: Эпизод 5 – Империя наносит ответный удар', 'Знакомьтесь; Джо Блэк', 'Рапунцель: Запутанная история', 'Старший сын', 'Вверх', 'Билли Эллиот', 'Мулан', 'Поющие под дождем', 'Жизнь Пи', 'Русалочка', 'Реквием по мечте', 'Гаттака', 'Догвилль', 'Мужики!..', 'Аты-баты; шли солдаты...', 'История игрушек: Большой побег', 'Леди и бродяга', 'Мандарины', 'Крамер против Крамера', 'Пираты Карибского моря: На краю Света', 'Иди и смотри', 'Профессионал', 'Холодное лето пятьдесят третьего...']
			bee=[]
			for e in r:
				ap = str(e)
				ap2= ap[7:-2]
				bee.append(ap2)
			for added in bee:			
				for s in mas:
					if s in added:
						kek = 'совпадение, такой фильм есть в бд'
						#return(render_template('myfilms_res.html', form=form, user=user, r=r,bee=bee, mas=mas ))
			return(render_template('myfilms_res2.html', form=form, user=user, r=r,bee=bee, mas=mas , film=film ))
	alls=Add_films.query.all()
	return(render_template('main.html', form=form,user=user,alls=alls))
	
@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
	form = SearchForm()
	user = {'user':"user1"}

	cursor=connection.cursor()
	sql= "SELECT * FROM table_name"
	cursor.execute(sql)
	results=cursor.fetchall()

	#print('отладка ',form.validate_on_submit() ,form.errors.items())
	if request.method == "POST":
		#print('отладка ',form.validate_on_submit() ,form.errors.items())
		if form.validate_on_submit():
			year = form.year.data 
			rating = form.rating.data
			print('form validate')
			global output_in_html
			output_in_html=[]

			if form.year.data != 'none' and form.rating.data != 'none':
				sql_request_search( request.form['year'], request.form['rating'] )
				itog = sql_request_search( request.form['year'], request.form['rating'] )
				
				for i in itog:
					output_in_html.append(i[0])
				return(render_template('search_results.html', output_in_html=output_in_html, user=user))
				
			elif request.form['year'] == 'none' and request.form['rating'] == 'none':
				flash('введите значения для поиска')

			elif request.form['year'] == 'none' and request.form['rating'] != 'none':
				sql_request_search( request.form['year'], request.form['rating'] )
				itog = sql_request_search( request.form['year'], request.form['rating'] )
				for i in itog:
					output_in_html.append(i[0])
				return(render_template('search_results.html', output_in_html=output_in_html, user=user))


			elif request.form['year'] != 'none' and request.form['rating'] == 'none':				
				sql_request_search( request.form['year'], request.form['rating'] )
				itog = sql_request_search( request.form['year'], request.form['rating'] )
				for i in itog:
					output_in_html.append(i[0])
				return(render_template('search_results.html', output_in_html=output_in_html, user=user))
	return(render_template("search_new.html", user=user, form=form))
	
@app.route("/actors")
@login_required
def actors():
	cursor=connection.cursor()
	sql= "SELECT * FROM table_name"
	cursor.execute(sql)
	results=cursor.fetchall()
	return(render_template("actors.html",results=results))	


@app.route("/top250")
@login_required
def top250():
	mas = []
	mov=[]
	cursor=connection.cursor()
	sql= "SELECT * FROM table_name"
	cursor.execute(sql)
	results = cursor.fetchall()
	return(render_template("top250.html",results=results, zip=zip))