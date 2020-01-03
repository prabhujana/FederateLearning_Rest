
from flask import Flask, request
import json
import requests
import ast
from model_train import train

app = Flask(__name__)

device_id = "http://localhost:8002"

@app.route('/')
def hello():
	return device_id

@app.route('/sendstatus', methods=['GET'])
def send_status():
	api_url = 'http://localhost:8000/clientstatus'

	data = {'client_id': '8002'}
	print(data)

	r = requests.post(url=api_url, json=data)
	print(r, r.status_code, r.reason, r.text)
	if r.status_code == 200:
		print("Ready to dsend")

	return "Status OK sent !"

@app.route('/sendmodel')
def send_model():
	file = open("local_model/mod2.npy", 'rb')
	data = {'fname':'model2.npy', 'id':'http://localhost:8002/'}
	files = {
		'json': ('json_data', json.dumps(data), 'application/json'),
		'model': ('model2.npy', file, 'application/octet-stream')
	}

	req = requests.post(url='http://localhost:8000/cmodel',	files=files)
	print("Model sent !")

@app.route('/aggmodel', methods=['POST'])
def get_agg_model():
	if request.method == 'POST':
		file = request.files['model'].read()
		fname = request.files['json'].read()

		fname = ast.literal_eval(fname.decode("utf-8"))
		fname = fname['fname']
		print(fname)

		wfile = open("model_update/"+fname, 'wb')
		wfile.write(file)

		print("Model received!")
		return "done"
	else:
		print("No file received!")

@app.route('/modeltrain')
def model_train():
	train()
	print("Model trained successfully!")
	send_status()
	send_model()
	return device_id


if __name__ == '__main__':
	app.run(host='localhost', port=8002, debug=False, use_reloader=True)
