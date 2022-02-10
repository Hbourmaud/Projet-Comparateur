from concurrent.futures import process
from inspect import _void
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	import requests
	game = "minecraft"
	if request.method == 'POST':
		game = request.form.get('search', '')
		game = game.replace(" ","-")

	print(game)
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
		'x-rapidapi-key': "577c741b61msh1de80c6b8100fdfp140b3cjsnd8d751d72ad8"
	}
	responseimg = requests.request("GET", urlimg, headers=headersimg, params=querystringimg)
	response= requests.request("GET", url, headers=headers, params=querystring)
	imggame = jprint(responseimg.json()['value'][0]['url'])
	print(imggame)
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
	
	return render_template('index.html',imggame = imggame,game = game,plat1 = tabplat[0],plat2 = tabplat[1],plat3 = tabplat[2],price1=tabprice[0],price2=tabprice[1],price3=tabprice[2],url1= taburl[0],url2= taburl[1],url3= taburl[2])


@app.route('/account', methods=['GET', 'POST'])
def account_page():
	import mysql.connector
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
		usr_usr= ("users",usrname)
		if (create_account == "on"):
			verif_SQL = """SELECT %s FROM accounts WHERE (users = %s)"""
			cursor.execute(verif_SQL,usr_usr)
			cursor.fetchall()
			if (cursor.rowcount >0):
				answer = "That username is taken. Try another."
			else:
				insert_SQL = """INSERT INTO accounts (id, users, password) VALUES (%s,%s,%s)"""
				cursor.execute(insert_SQL, usr_info)
				answer = "Your account has been created successfully !"
		db.commit()
		cursor.close()
		db.close()
	
	return render_template('account.html', answer=answer)
def jprint(obj):
	import json
	text = json.dumps(obj, sort_keys=True, indent=4)
	return(text)

if __name__ == "__main__":
    app.run(host='164.132.230.224')
