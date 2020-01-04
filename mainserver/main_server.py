from flask import Flask, request
import requests, json
import ast
from fl_agg import model_aggregation

app = Flask(__name__)

workers = []

def reg_workers():
	return workers

@app.route('/register', methods=['POST'])
def register_worker():
		if request.method == 'POST':
			worker_id = request.data.decode('UTF-8')
			if worker_id not in workers:
				workers.append(request.data.decode('UTF-8'))
				print(workers)
			return "Worker Registered"

@app.route('/secagg_model', methods=['POST'])
def get_secagg_model():
	if request.method == 'POST':
		file = request.files['model'].read()
		fname = request.files['json'].read()
		fname = ast.literal_eval(fname.decode("utf-8"))
		cli = fname['id']+'\n'
		fname = fname['fname']
		wfile = open("agg_model/"+fname, 'wb')
		wfile.write(file)
		return "Model received!"
	else:
		return "No file received!"

@app.route('/cmodel', methods=['POST'])
def getmodel():
	if request.method == 'POST':
		file = request.files['model'].read()
		fname = request.files['json'].read()
		fname = ast.literal_eval(fname.decode("utf-8"))
		cli = fname['id']+'\n'
		fname = fname['fname']
		print(fname)
		wfile = open("client_models/"+fname, 'wb')
		wfile.write(file)
		return "Model received!"
	else:
		return "No file received!"

@app.route('/aggregate_models')
def perform_model_aggregation():
	model_aggregation()
	return 'Model aggregation done!\nGlobal model written to persistent storage.'

@app.route('/send_model_clients')
def send_agg_to_clients(i):
	clients = []
	clients.append(i)
	print('Clients:',clients)

	for c in clients:
		if c != '':
			file = open("agg_model/agg_model.h5", 'rb')
			data = {'fname':'agg_model.h5'}
			files = {
				'json': ('json_data', json.dumps(data), 'application/json'),
				'model': ('agg_model.h5', file, 'application/octet-stream')
			}
			print(c+'/aggmodel')
			req = requests.post(url=c+'/aggmodel', files=files)
			print(req.status_code)
	return "Aggregated model sent !"

@app.route('/send_agg_to_client')
def send_agg_to_client(client):
	if client != '':
		file = open("agg_model/agg_model.h5", 'rb')
		data = {'fname':'agg_model.h5'}
		files = {
			'json': ('json_data', json.dumps(data), 'application/json'),
			'model': ('agg_model.h5', file, 'application/octet-stream')
		}
		print(c+'aggmodel')
		req = requests.post(url=c+'/aggmodel', files=files)
		print(req.status_code)
	return "Aggregated model sent !"

if __name__ == '__main__':
	app.run(host='localhost', port=8000, debug=False, use_reloader=True)
