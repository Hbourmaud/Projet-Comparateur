from concurrent.futures import process
from inspect import _void
from multiprocessing.dummy import Array
import mysql.connector
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "any random string"

@app.route('/', methods=['GET','POST'])
def index():
	answer = ""
	try:
		name = session['name']
	except:
		name = "Not login"
	return render_template('index.html', name=name,answer = answer)

@app.route('/search', methods=['POST'])
def search_page():
	import requests
	game = request.form.get('search', '')
	game = game.replace(" ","-")
	try:
		name = session['name']
		id_usr = session['id_usr']
	except:
		name = "Not login"
		id_usr = -1
	try:
		st_like = request.form['like_btn']
	except:
		st_like = "No action"	
	
	if (st_like != "No action"):
			imggame = session['fav_imggame']
			game = session['fav_game']
			tabplat = session['tab_plat']
			tabprice = session['tab_price']
			taburl = session['tab_url']

	if (id_usr == -1):
			answer = "Log in to an account for add games to in favorites list"
			heart = "💗"
	else:
		heart="💗"
		db = mysql.connector.connect(
		host="164.132.230.213",
		database="comparator",
		user="supadmin",
		password="supadmin00SQL"
		)
		cursor = db.cursor()
		verifgames_sql = """SELECT games FROM gaming WHERE (id =%s) AND (games =%s);"""
		id_games_tup = (id_usr,game)
		cursor.execute(verifgames_sql,id_games_tup)
		cursor.fetchall()
		if (cursor.rowcount == 0):
			if (st_like != "No action") :
				answer = "Game add to your favorites list"
				insert_SQL = """INSERT INTO gaming (id, games, sources, price, technology_plateforms) VALUES (%s,%s,%s,%s,%s)"""
				addfav_tuple = (id_usr,game,imggame,tabprice[0],taburl[0])
				cursor.execute(insert_SQL,addfav_tuple)
				heart = "💔"
		elif (st_like != "No action") :
			remov_fav_SQL = """DELETE FROM gaming WHERE (id =%s) AND (games =%s);"""
			cursor.execute(remov_fav_SQL,id_games_tup)
			answer= "This game has been removed from your favorites list!"
			heart = "💗"
		else:
			heart = "💔"
		db.commit()
		cursor.close()
		db.close()

	if (st_like == "No action"):
		answer = ""
		url = "https://game-prices.p.rapidapi.com/game/"+game
		urlimg ="https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/ImageSearchAPI"
		querystringimg = {"q":game,"pageNumber":"1","pageSize":"1","autoCorrect":"true","safeSearch":"true"}
		querystring = {"region":"fr","type":"game"}
		headersimg = {
		'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com",
		'x-rapidapi-key': "577c741b61msh1de80c6b8100fdfp140b3cjsnd8d751d72ad8"
		}
		headers = {
			'x-rapidapi-host': "game-prices.p.rapidapi.com",
			'x-rapidapi-key': "d2abd07233msh342d8cc4910aac3p15ac81jsnb755f63983c0"
		}
		response= requests.request("GET", url, headers=headers, params=querystring)
		if (len(response.json()) < 4):
			return render_template('index.html',name = name,answer = "No Game found sorry :(")
		responseimg = requests.request("GET", urlimg, headers=headersimg, params=querystringimg)
		imggame = jprint(responseimg.json()['value'][0]['url'])
		price1r = jprint(response.json()['stores'][0]["price"])
		price2r = jprint(response.json()['stores'][1]["price"])
		price3r = jprint(response.json()['stores'][2]["price"])
		price1plat = jprint(response.json()['stores'][0]["seller"])
		price2plat = jprint(response.json()['stores'][1]["seller"])
		price3plat = jprint(response.json()['stores'][2]["seller"])
		url1 = jprint(response.json()['stores'][0]["url"])
		url2 = jprint(response.json()['stores'][1]["url"])
		url3 = jprint(response.json()['stores'][2]["url"])
		url1 = url1[1:-1]
		url2 = url2[1:-1]
		url3 = url3[1:-1]
		imggame = imggame[1:-1]
		tabprice = [price1r,price2r,price3r]
		tabplat = [price1plat,price2plat,price3plat]
		taburl = [url1,url2,url3]
		if price1r > price2r:
			tabprice[0] = price2r
			tabplat[0] = price2plat
			taburl[0] = url2
			tabprice[1] = price1r
			tabplat[1] = price1plat
			taburl[1] = url1
		if price1r > price3r:
			tabprice[1] = price3r
			tabplat[1] = price3plat
			taburl[1] = url3
			tabprice[2] = price1r
			tabplat[2] = price1plat
			taburl[2] = url1
			
		if price2r > price3r:
			tabprice[0] = price3r
			tabplat[0] = price3plat
			taburl[0] = url3
			tabprice[1] = price2r
			tabplat[1] = price2plat
			taburl[1] = url2

		session['fav_imggame'] = imggame
		session['fav_game'] = game
		session['tab_plat'] = tabplat
		session['tab_price'] = tabprice
		session['tab_url'] = taburl

	return render_template('search.html',heart = heart,answer = answer,name = name,imggame = imggame,game = game,plat1 = tabplat[0],plat2 = tabplat[1],plat3 = tabplat[2],price1=tabprice[0],price2=tabprice[1],price3=tabprice[2],url1= taburl[0],url2= taburl[1],url3= taburl[2])


@app.route('/account', methods=['GET', 'POST'])
def account_page():
	try:
		name = session['name']
	except:
		name = "Not login"
	answer = ""
	create_account = "off"
	if request.method == 'POST':
		usrname = request.form['username']
		passwd = request.form['passwd']
		try:
			create_account = request.form['create']
		except:
			pass
		db = mysql.connector.connect(
		host="164.132.230.213",
		database="comparator",
		user="supadmin",
		password="supadmin00SQL"	
		)
		cursor = db.cursor()
		cursor.execute("SELECT * from accounts")
		cursor.fetchall()
		count_row = cursor.rowcount
		usr_info= (count_row,usrname, passwd)
		usr_usr= (usrname,)
		usr_pswd = (usrname,passwd)
		if (create_account == "on"):
			verif_SQL = """SELECT users FROM accounts WHERE (users = %s)"""
			cursor.execute(verif_SQL,usr_usr)
			cursor.fetchall()
			if (cursor.rowcount >0):
				answer = "That username is taken. Try another."
			else:
				insert_SQL = """INSERT INTO accounts (id, users, password) VALUES (%s,%s,%s)"""
				cursor.execute(insert_SQL, usr_info)
				answer = "Your account has been created successfully !"
				session['name'] = usrname
				session['id_usr'] = usr_info[0]
				db.commit()
				cursor.close()
				db.close()
				return render_template('index.html',name = name ,answer = answer)
		else:
			verifacc_SQL = """SELECT * FROM accounts WHERE (users = %s) AND password = %s"""
			cursor.execute(verifacc_SQL, usr_pswd)
			row = cursor.fetchall()
			if (cursor.rowcount != 1):
				answer = "Username or Password incorrect. Please Retry!"
			else:
				print("row",row[0][0])
				answer = "Successfully login!"
				session['name'] = usrname
				session['id_usr'] = row[0][0]
				db.commit()
				cursor.close()
				db.close()
				return render_template('index.html',name = name,answer = answer)
		db.commit()
		cursor.close()
		db.close()
	
	return render_template('account.html', answer=answer, name = name)


@app.route('/favorites', methods=['GET','POST'])
def favorites():
	fav_games = []
	list_fav_games =[]
	try:
		name = session['name']
	except:
		name = "Not login"
	if (name=="Not login"):
		answer = "Please login to access the favorites features "
	else:
		id_usr = session['id_usr']
		db = mysql.connector.connect(
		host="164.132.230.213",
		database="comparator",
		user="supadmin",
		password="supadmin00SQL"	
		)
		answer = "Your favorites games :"
		cursor = db.cursor()
		if request.method == 'POST':
			game_del = request.form['game_del']
			remov_fav_SQL = """DELETE FROM gaming WHERE (id = %s) AND (games = %s);"""
			id_games_tup = (id_usr,game_del)
			cursor.execute(remov_fav_SQL,id_games_tup)
		cursor = db.cursor()
		gam_usr = (session['id_usr'],)
		fav_SQL = """SELECT * FROM gaming WHERE (id = %s);"""
		cursor.execute(fav_SQL,gam_usr)
		info_games = cursor.fetchall()
		print(info_games)
		if (cursor.rowcount == 0):
			answer = "No games in favorites"
		else:
			for k in range(0,cursor.rowcount):
				fav_games.append(info_games[k][1])
				fav_games.append(info_games[k][2])
				fav_games.append(info_games[k][3])
				fav_games.append(info_games[k][4])
				list_fav_games.append(fav_games)
				fav_games = []
		db.commit()
		cursor.close()
		db.close()
	return render_template('favorites.html',len=len(list_fav_games),infoG = list_fav_games, answer=answer, name=name)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
	session.pop('name',"Not login")
	session.pop('id_usr',-1)
	name = "Not login"
	return render_template('index.html',name = name,answer = "You are now logged out")

def jprint(obj):
	import json
	text = json.dumps(obj, sort_keys=True, indent=4)
	return(text)

if __name__ == "__main__":
    app.run(host='164.132.230.224')
