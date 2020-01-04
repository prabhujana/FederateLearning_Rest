
from flask import Flask, request
from flask_script import Manager
import json
import requests
import ast
from model_train import train
import argparse
import sys

app = Flask(__name__)
#manager = Manager(app)

@app.route('/')
def hello():
	return device_id

def register_with_agg():
	data1 = {'workerid' : device_id}
	res = requests.post(url='http://'+ agg + ':' + str(8000) + '/register', data = device_id)
	print(res.text)

@app.route('/sendmodel')
def send_model():
	file = open("local_model/mod2.npy", 'rb')
	#data = {'fname':'model2.npy', 'id':'http://localhost:8002/'}
	data = {'fname': 'model2.npy', 'id': device_id}
	files = { 'json': ('json_data', json.dumps(data), 'application/json'), 'model': ('model2.npy', file, 'application/octet-stream') }
	req = requests.post(url='http://'+ agg + ':' + str(8000) + '/cmodel', files=files)
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
	send_model()
	return device_id

def define_and_get_arguments(args=sys.argv[1:]):
    # Parse args
    parser = argparse.ArgumentParser(description="Run FL worker")
    parser.add_argument("--host", type=str, default="localhost", help="IP of local worker")
    parser.add_argument("--workerid", type=int, default=1, help="worker id e.g. --id 1")
    parser.add_argument("--agg", type=str, default="localhost", help="IP of Aggregator")
    parser.add_argument("--port","-p",type=int, default=8000, help="port number of aggregator, e.g. --port 8777",)
    args = parser.parse_args(args=args)
    return args

#@manager.command
def run_worker():
	register_with_agg()
	app.run(host=host, port=int(host_port), debug=False, use_reloader=True)

if __name__ == '__main__':
	args = define_and_get_arguments(sys.argv[1:])
	host = args.host
	workerid = args.workerid
	host_port = int(8000+workerid)
	port = args.port
	agg = args.agg
	device_id = "http://" + host + ':' + str(host_port)
	run_worker()
