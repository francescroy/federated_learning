
import requests
import time
import numpy as np

url = 'http://127.0.0.1:5000'
#url = 'http://10.139.40.19:5000'

########################################
########################################
########################################

class TrainingClient:
    def __init__(self, client_url):
        self.client_url = client_url

        self.learning_rate = None
        self.epochs = None
        self.batch_size = None
        self.training_images = None
        self.test_images = None

        self.losses = []
        self.accuracies = []
        self.test_losses = []
        self.test_accuracies = []

        self.init_training_time = []
        self.end_training_time = []

        self.workload_rythm = []

    def get_mean_training_time(self,time_window):

        last_window_slice_init = np.array(self.init_training_time[-time_window::])
        last_window_slice_end = np.array(self.end_training_time[-time_window::])

        last_window_time = last_window_slice_end - last_window_slice_init

        return np.mean(last_window_time)

    def get_mean_workload_rythm(self,time_window):

        last_window_workload_rythm = np.array(self.workload_rythm[-time_window::])

        return np.mean(last_window_workload_rythm)

    def get_last_training_time(self):

        return self.end_training_time[-1::][0] - self.init_training_time[-1::][0]

########################################
########################################
########################################

class Server:
    def __init__(self):
        self.training_clients = {}
        self.learning_rate = 0.0000001
        self.epochs = 1
        self.batch_size = 32
        self.training_images = 400
        self.test_images = 200
        self.tempos_rounds = []
        self.round = 0

server = Server()

def convert_dictionary_to_object(dict):

    tr_client = TrainingClient(dict['client_url'])

    tr_client.learning_rate = dict['learning_rate']
    tr_client.epochs = dict['epochs']
    tr_client.batch_size = dict['batch_size']
    tr_client.training_images = dict['training_images']
    tr_client.test_images = dict['test_images']

    tr_client.losses = dict['losses']
    tr_client.accuracies = dict['accuracies']
    tr_client.test_losses = dict['test_losses']
    tr_client.test_accuracies = dict['test_accuracies']

    tr_client.init_training_time = dict['init_training_time']
    tr_client.end_training_time = dict['end_training_time']

    tr_client.workload_rythm = dict['workload_rythm']

    return tr_client

def fill_training_clients(server, x):
    for i in range(len(x.json())):
        obj = convert_dictionary_to_object(x.json()[i])
        #print(obj.workload_rythm)

        server.training_clients[obj.client_url] = obj

def decide_number_of_images_for_next_round(training_clients, server_training_images, time_window):

    worst_client = list(training_clients.values())[0]

    for client in training_clients.values():
        if client.get_mean_workload_rythm(time_window) < worst_client.get_mean_workload_rythm(time_window):
            worst_client= client

    #print(worst_client.get_mean_workload_rythm(time_window))

    for client in training_clients.values():
        if client.training_images is None:
            client.training_images = server_training_images

    for client in training_clients.values():
        if client.client_url != worst_client.client_url:
            #if client.get_mean_training_time(time_window) < worst_client.get_mean_training_time(time_window):
            if client.get_last_training_time() < worst_client.get_last_training_time():
                #client.training_images = client.training_images + 10
                requests.post(url + "/set_epochs_lr_batchsize_training_test_for_client",
                              data={'epochs': 'None', 'lr': 'None','batchsize':'None', 'training': str(client.training_images + 10),'test':'None','clienturl': str(client.client_url)})








round=0

while round< 10:

    round = round + 1

    ## Here:
    x = requests.get(url + "/get_training_clients")
    fill_training_clients(server, x)

    #print(server.training_clients['http://localhost:5001'].workload_rythm)

    if round > 3:
        decide_number_of_images_for_next_round(server.training_clients, server.training_images,3)



    requests.post(url+"/training", json = {'training_type': 'CHEST_X_RAY_PNEUMONIA'}, headers = {"Content-Type": "application/json"})
    print("Ronda ",round," completada.")

    time.sleep(2.0)









#x = requests.get(url+"/get_tempos_and_accuracies")
#print(x.json())




