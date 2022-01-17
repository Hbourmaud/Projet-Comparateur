from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    import requests
    import json
    response = requests.get("http://store.steampowered.com/api/appdetails?appids=1295900&filters=price_overview")
    price = jprint(response.json()['1295900']['data']['price_overview']['final'])
    return render_template('index.html', price=price)

def jprint(obj):
	import json
	text = json.dumps(obj, sort_keys=True, indent=4)
	return(text)
