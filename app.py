from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    import requests
    import json
    game = "cyberpunk"
    url = "https://best-game-price-search.p.rapidapi.com/allshops/"+ game
    headers = {
        'x-rapidapi-host': "best-game-price-search.p.rapidapi.com",
        'x-rapidapi-key': "577c741b61msh1de80c6b8100fdfp140b3cjsnd8d751d72ad8"
	}
    response= requests.request("GET", url, headers=headers)
    price1 = jprint(response.json()[1]["Steam"][0]["price"])
    price2 = jprint(response.json()[2]["Epic"][0]["price"])
    price3 = jprint(response.json()[4]["Instant Gaming"][0]["price"])
    priceSt = float(price1[7:-1])
    priceE = float(price2[7:-1])
    priceI = float(price3[7:-1])
    price1 = {"plat":"Steam" , "price":priceSt}
    price2 = {"plat":"Epic", "price":priceE}
    price3 = {"plat":"Instant Gaming", "price":priceI}
    prices = [price1["price"],price2["price"],price3["price"]]
    plat1 = ""
    plat2 = ""
    plat3 = ""
    plats = [plat1,plat2,plat3]
    prices.sort()
    print(prices)
    for x in range(0,3):
    	if prices[x] == price1["price"] and prices[x] != price2["price"] and prices[x] != price3["price"]:
    		plats[x] = price1["plat"]
    	elif prices[x] == price2["price"] and prices[x] != price1["price"] and prices[x] != price3["price"]:
    		plats[x] = price2["plat"]
    	elif prices[x] == price3["price"] and prices[x] != price1["price"] and prices[x] != price2["price"]:
    		plats[x] = price3["plat"]
    	elif prices[x] == price1["price"] and prices[x] == price2["price"] and prices[x] == price3["price"]:
    		plats[0] = price1["plat"]
    		plats[1] = price1["plat"]
    		plats[2] = price1["plat"]
    return render_template('index.html',plat1 = plats[0], plat2 = plats[1], plat3 = plats[2], price=prices[0], price2=prices[1], price3=prices[2])

def jprint(obj):
	import json
	text = json.dumps(obj, sort_keys=True, indent=4)
	return(text)
