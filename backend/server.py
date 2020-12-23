from flask import Flask, request
from flask_cors import CORS, cross_origin
import json
from ad_search import AdSearch
from ad_search import neuroSearch



app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
	return 'Hello'


@app.route('/get')
@cross_origin()
def get():
	search = AdSearch(request.args.get('v', None))
	return search.find()


@app.route('/ad')
@cross_origin()
def ad():
	text = request.args.get('text', None)
	res = 0
	if text == 'Рекламная пауза':
		res = 1
	else:
		res = neuroSearch.predict_with_parse(text)
		#if res:
		#	res = 1
		#else:
		#	res = 0
	return {'subtitle' : res}


@app.route('/evaluate')
@cross_origin()
def evaluate():
	search = AdSearch('')
	search.evaluate_ranges()
	return {'' : ''}


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)
