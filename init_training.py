
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

        self.status = None

        self.model_params = None

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

        self.jumps = [1,3,6,12,25,50,100]
        self.last_jump_sign = +1

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
        self.mnist_model_params = None
        self.chest_x_ray_model_params = None
        self.training_clients = {}
        self.status = None
        self.learning_rate = 0.000001
        self.epochs = 1
        self.batch_size = 4
        self.training_images = 50
        self.test_images = 25
        self.tempos_rounds = []
        self.round = 0

server = Server()

worst_client_last_round = None

def add_or_update_client(dict):

    tr_client = server.training_clients.get(dict['client_url'])

    if tr_client is None:
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

    server.training_clients[dict['client_url']] = tr_client

def fill_training_clients(x):
    for i in range(len(x.json())):
        add_or_update_client(x.json()[i])
        #print(obj.workload_rythm)

def decide_number_of_images_for_next_round(training_clients, time_window):
    global worst_client_last_round

    worst_client = list(training_clients.values())[0]

    for client in training_clients.values():
        if client.get_mean_workload_rythm(time_window) < worst_client.get_mean_workload_rythm(time_window):
            worst_client = client

    if worst_client_last_round is not None:
        if worst_client_last_round.client_url != worst_client.client_url:
            for client in training_clients.values():
                requests.post(url + "/set_epochs_lr_batchsize_training_test_for_client",
                  data={
                      'epochs': 'None',
                      'lr': 'None',
                      'batchsize': 'None',
                      'training': str(server.training_images),
                      'test': 'None',
                      'clienturl': str(client.client_url)
                    }
                  )

            for client in training_clients.values():
                client.jumps = [1, 3, 6, 12, 25, 50, 100]
                client.last_jump_sign = +1

        else:

            for client in training_clients.values():
                if client.client_url != worst_client.client_url:
                    #if client.get_mean_training_time(time_window) < worst_client.get_mean_training_time(time_window):
                    if client.get_last_training_time() < worst_client.get_last_training_time() - 1:

                        if client.last_jump_sign == -1:

                            if len(client.jumps) !=1:
                                client.jumps.pop()

                        requests.post(url + "/set_epochs_lr_batchsize_training_test_for_client",
                                      data={
                                            'epochs': 'None',
                                            'lr': 'None',
                                            'batchsize':'None',
                                            'training': str(client.training_images + client.jumps[len(client.jumps)-1]),
                                            'test':'None',
                                            'clienturl': str(client.client_url)
                                            }
                                      )

                        client.last_jump_sign = +1

                    elif client.get_last_training_time() > worst_client.get_last_training_time() + 1:

                        if client.last_jump_sign == +1:

                            if len(client.jumps) != 1:
                                client.jumps.pop()

                        requests.post(url + "/set_epochs_lr_batchsize_training_test_for_client",
                                      data={
                                          'epochs': 'None',
                                          'lr': 'None',
                                          'batchsize': 'None',
                                          'training': str(client.training_images - client.jumps[len(client.jumps) - 1]),
                                          'test': 'None',
                                          'clienturl': str(client.client_url)
                                        }
                                      )

                        client.last_jump_sign = -1

    worst_client_last_round = worst_client








time.sleep(1.0)

round=0

while round< 5000:

    round = round + 1

    x = requests.get(url + "/get_training_clients")
    fill_training_clients(x)

    if round==1:
        for client in server.training_clients.values():
            requests.post(url + "/set_epochs_lr_batchsize_training_test_for_client",
                          data={
                              'epochs': str(server.epochs),
                              'lr': str(server.learning_rate),
                              'batchsize': str(server.batch_size),
                              'training': str(server.training_images),
                              'test': str(server.test_images),
                              'clienturl': str(client.client_url)
                            }
                          )

    if round > 5:
        decide_number_of_images_for_next_round(server.training_clients,3)

    requests.post(url+"/training", json = {'training_type': 'CHEST_X_RAY_PNEUMONIA'}, headers = {"Content-Type": "application/json"})
    print("Ronda ",round," completada.")

    time.sleep(5.0)










#x = requests.get(url+"/get_tempos_and_accuracies")
#print(x.json())



