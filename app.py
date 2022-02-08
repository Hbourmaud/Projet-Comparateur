from concurrent.futures import process
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	import requests
	import json
	game = "minecraft"
	if request.method == 'POST':
		game = request.form.get('search', '')
		game = game.replace(" ","-")

	print(game)
	url = "https://game-prices.p.rapidapi.com/game/"+game
	querystring = {"region":"fr","type":"game"}
	headers = {
		'x-rapidapi-host': "game-prices.p.rapidapi.com",
		'x-rapidapi-key': "577c741b61msh1de80c6b8100fdfp140b3cjsnd8d751d72ad8"
	}
	response= requests.request("GET", url, headers=headers, params=querystring)
	price1r = jprint(response.json()['stores'][0]["price"])
	price2r = jprint(response.json()['stores'][1]["price"])
	price3r = jprint(response.json()['stores'][2]["price"])
	price1plat = jprint(response.json()['stores'][0]["seller"])
	price2plat = jprint(response.json()['stores'][1]["seller"])
	price3plat = jprint(response.json()['stores'][2]["seller"])
	tabprice = [price1r,price2r,price3r]
	tabplat = [price1plat,price2plat,price3plat]
	if price1r > price2r:
		tabprice[0] = price2r
		tabplat[0] = price2plat
		tabprice[1] = price1r
		tabplat[1] = price1plat
	if price1r > price3r:
		tabprice[1] = price3r
		tabplat[1] = price3plat
		tabprice[2] = price1r
		tabplat[2] = price1plat
	if price2r > price3r:
		tabprice[0] = price3r
		tabplat[0] = price3plat
		tabprice[1] = price2r
		tabplat[1] = price2plat
	
	return render_template('index.html',game = game,plat1 = tabplat[0],plat2 = tabplat[1],plat3 = tabplat[2],price1=tabprice[0],price2=tabprice[1],price3=tabprice[2])


@app.route('/account', methods=['GET', 'POST'])
def account_page():
	if request.method == 'GET':
		return render_template('account.html')

def jprint(obj):
	import json
	text = json.dumps(obj, sort_keys=True, indent=4)
	return(text)

