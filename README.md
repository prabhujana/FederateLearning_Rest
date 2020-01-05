This work is enhanced with previous works from 

# Fedlearn - https://github.com/adesgautam/Fedlearn
# FederateLearning_Rest - https://github.com/pinyaras/FederateLearning_Rest


An implementation to simulate a Asynchronous federated learning environment.

### Tech stack
* Python 3.6.1
* Keras
* Flask

## Run the system using the steps below:
## Booting up for local simulation

# Worker
1. Go to folder `Device1`. Run "Device1" using `python app.py --host localhost --workerid 1 --agg localhost --port 8000`. Device1 will be worker. Device1 Rest server will be functional (eg: http://localhost:8001 ). 

Access help by using `python app.py --help`.

Worker port number is determined based on the --workerid. To run multiple workers, just copy folder Device1 and create new folder for each worker.

# Aggregator
2. Go to folder `Main Server`. Run "Main Server" using `python main_server.py`. This will instantiate REST services on Main server or aggregator.

3. You can start asynchronous training using `python train_async.py`

This will start the Flask servers of the two devices and the main server.

Servers - 
* Main server - `http://localhost:8000/`
* Worker - `http://localhost:8001/`

Everything will work using the REST APIs. 
