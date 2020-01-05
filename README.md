This work is enhanced with previous works from 

# Fedlearn - https://github.com/adesgautam/Fedlearn
# FederateLearning_Rest - https://github.com/pinyaras/FederateLearning_Rest


An implementation to simulate a Asynchronous federated learning environment.

### Tech stack
* Python 3.6.1
* Keras
* Flask

## Run the system using the steps below:
### Booting up for local simulation
1. Run "Device1" using `python app.py --host localhost --workerid 1 --agg localhost --port 8000`.
   Device1 Rest server will be functional (eg: http://localhost:8001 ) Access help by using `python app.py --help`.
   
   Worker port number is determined based on the --workerid.
   
   To run multiple workers, just copy folder Device1 and create new folder for each worker. 

2. Run "Main Server" using `python main_server.py`. This will instantiate REST services on Main server or aggregator.

3. You can start asynchronous training using `python train_async.py`


This will start the Flask servers of the two devices and the main server.

Servers - 
* Main server - `http://localhost:8000/`
* Worker - `http://localhost:8001/`


Everything will work using the REST APIs. 

### System working
1. First a model will be trained locally on the device.
On 'Device1' and 'Device2' server navigate to: `http://localhost:8001/modeltrain` and `http://localhost:8002/modeltrain` respectively.

The models will be trained on MNIST data.

2. Once the devices are ready send a status signal to the server that they are ready, using, `http://localhost:8001/sendstatus` and `http://localhost:8002/sendstatus`.

There will be a response from the main server.

3. Now, the trained models will be sent to the aggregator server using `http://localhost:8001/sendmodel` and `http://localhost:8002/sendmodel`

4. The main server will send the aggregated model to the devices.

5. `http://localhost:8000/send_model_clients`

6. Goto step 1. The whole process is repeated again and the aggregated global model is improved at every round.
