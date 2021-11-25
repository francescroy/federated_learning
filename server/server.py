import asyncio
import sys
import aiohttp
import torch

import numpy as np

import time

import copy

from .utils import model_params_to_request_params
from .federated_learning_config import FederatedLearningConfig
from .client_training_status import ClientTrainingStatus
from .server_status import ServerStatus
from .training_client import TrainingClient
from .training_type import TrainingType


class Server:
    def __init__(self):
        self.mnist_model_params = None
        self.chest_x_ray_model_params = None
        self.init_params()
        self.training_clients = {}
        self.status = ServerStatus.IDLE
        self.learning_rate = 0.0001
        self.epochs = 100
        self.batch_size = 2
        self.training_images = 100
        self.test_images = 50
        self.tempos_rounds = []
        self.round = 0
        self.version = 0

    def init_params(self):
        if self.mnist_model_params is None:
            weights = torch.randn((28 * 28, 1), dtype=torch.float, requires_grad=True)
            bias = torch.randn(1, dtype=torch.float, requires_grad=True)
            self.mnist_model_params = weights, bias

    async def start_training(self, training_type):
        successful_training = False

        if self.status != ServerStatus.IDLE:
            print('Server is not ready for training yet, status:', self.status)
        elif len(self.training_clients) == 0:
            print("There aren't any clients registered in the system, nothing to do yet")
        else:
            self.round = self.round+1
            print("\n\n\n\n\nRound: ",self.round,"\n\n\n\n\n")

            request_body = {}
            federated_learning_config = None
            if training_type == TrainingType.MNIST:
                request_body = model_params_to_request_params(training_type, self.mnist_model_params)
                federated_learning_config = FederatedLearningConfig(self.learning_rate, self.epochs, self.batch_size, self.training_images, self.test_images)
            elif training_type == TrainingType.CHEST_X_RAY_PNEUMONIA:
                request_body = model_params_to_request_params(training_type, self.chest_x_ray_model_params)
                federated_learning_config = FederatedLearningConfig(self.learning_rate, self.epochs, self.batch_size, self.training_images, self.test_images)

            request_body['learning_rate'] = federated_learning_config.learning_rate
            request_body['epochs'] = federated_learning_config.epochs
            request_body['batch_size'] = federated_learning_config.batch_size
            request_body['training_images'] = federated_learning_config.training_images
            request_body['test_images'] = federated_learning_config.test_images

            request_body['training_type'] = training_type

            print('There are', len(self.training_clients), 'clients registered')
            tasks = []
            for training_client in self.training_clients.values():
                tasks.append(asyncio.ensure_future(self.do_training_client_request(training_type, training_client, request_body)))
            print('Requesting training to clients...')
            self.status = ServerStatus.CLIENTS_TRAINING
            await asyncio.gather(*tasks)
            successful_training = True
        sys.stdout.flush()
        return successful_training

    def modify_request_body_for_client(self, training_client, request_body):

        if training_client.learning_rate is not None:
            request_body['learning_rate'] = training_client.learning_rate
        if training_client.epochs is not None:
            request_body['epochs'] = training_client.epochs
        if training_client.batch_size is not None:
            request_body['batch_size'] = training_client.batch_size
        if training_client.training_images is not None:
            request_body['training_images'] = training_client.training_images
        if training_client.test_images is not None:
            request_body['test_images'] = training_client.test_images

        return request_body

    async def do_training_client_request(self, training_type, training_client, request_body):

        # Let's mark when the client starts training:
        training_client.init_training_time.append(time.time())

        request_body = self.modify_request_body_for_client(training_client, copy.deepcopy(request_body))

        request_url = training_client.client_url + '/training'

        timeout = aiohttp.ClientTimeout(total=600) # A round will never last more than 600 seconds
        print('Requesting training to client', request_url)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            training_client.status = ClientTrainingStatus.TRAINING_REQUESTED
            async with session.post(request_url, json=request_body) as response:
                if response.status != 200:
                    print('Error requesting training to client', training_client.client_url)
                    training_client.status = ClientTrainingStatus.TRAINING_REQUEST_ERROR
                    self.update_server_model_params(training_type)
                else:
                    print('Client', training_client.client_url, 'started training')

    def update_client_model_params(self, training_type, training_client, client_model_params):
        print('New model params received from client', training_client.client_url)
        training_client.model_params = client_model_params

        # Let's mark when the client ends training:
        training_client.end_training_time.append(time.time())

        if self.version ==0:
            pass # fed learning baseline, does not need to collect rythms
        elif self.version==1:
            training_client.add_workload_rythm(self.training_images, self.round, self.version)
        elif self.version==2:
            training_client.add_workload_rythm(self.epochs, self.round, self.version)

        training_client.status = ClientTrainingStatus.TRAINING_FINISHED
        self.update_server_model_params(training_type)

    def update_server_model_params(self, training_type):
        if self.can_update_central_model_params():
            print('Updating global model params')

            self.tempos_rounds.append(time.time())
            print("Tempos: ",self.get_list_tempos())

            self.status = ServerStatus.UPDATING_MODEL_PARAMS
            if training_type == TrainingType.MNIST:
                received_weights = []
                received_biases = []
                for training_client in self.training_clients.values():
                    if training_client.status == ClientTrainingStatus.TRAINING_FINISHED:
                        received_weights.append(training_client.model_params[0])
                        received_biases.append(training_client.model_params[1])
                        training_client.status = ClientTrainingStatus.IDLE
                new_weights = torch.stack(received_weights).mean(0)
                new_bias = torch.stack(received_biases).mean(0)
                self.mnist_model_params = new_weights, new_bias
                print('Model weights for', TrainingType.MNIST, 'updated in central model')
            elif training_type == TrainingType.CHEST_X_RAY_PNEUMONIA:
                received_weights = []
                for training_client in self.training_clients.values():
                    if training_client.status == ClientTrainingStatus.TRAINING_FINISHED:
                        training_client.status = ClientTrainingStatus.IDLE
                        received_weights.append(training_client.model_params)
                new_weights = np.stack(received_weights).mean(0)
                self.chest_x_ray_model_params = new_weights
                print('Model weights for', TrainingType.CHEST_X_RAY_PNEUMONIA, 'updated in central model')
            self.status = ServerStatus.IDLE
        sys.stdout.flush()

    def can_update_central_model_params(self):
        for training_client in self.training_clients.values():
            if training_client.status != ClientTrainingStatus.TRAINING_FINISHED \
                    and training_client.status != ClientTrainingStatus.TRAINING_REQUEST_ERROR:
                return False
        return True

    def register_client(self, client_url):
        print('Registering new training client [', client_url, ']')
        if self.training_clients.get(client_url) is None:
            self.training_clients[client_url] = TrainingClient(client_url)
            print('Client [', client_url, '] registered successfully')
        else:
            print('Client [', client_url, '] was already registered in the system')
            self.training_clients.get(client_url).status = ClientTrainingStatus.IDLE
        sys.stdout.flush()

    def unregister_client(self, client_url):
        print('Unregistering client [', client_url, ']')
        try:
            self.training_clients.pop(client_url)
            print('Client [', client_url, '] unregistered successfully')
        except KeyError:
            print('Client [', client_url, '] is not registered yet')
        sys.stdout.flush()

    def can_do_training(self):
        for training_client in self.training_clients.values():
            if training_client.status != ClientTrainingStatus.IDLE \
                    and training_client.status != ClientTrainingStatus.TRAINING_REQUEST_ERROR:
                return False

        return True

    def set_epochs_lr_batchsize_training_test(self,epochs,learning_rate,batch_size,training_images,test_images):
        if (epochs!= 'None'): self.epochs = int(epochs.strip())
        if (learning_rate!= 'None'): self.learning_rate = float(learning_rate.strip())
        if (batch_size!= 'None'): self.batch_size = int(batch_size.strip())
        if (training_images!= 'None'): self.training_images = int(training_images.strip())
        if (test_images!= 'None'): self.test_images = int(test_images.strip())

    def set_epochs_lr_batchsize_training_test_for_client(self, epochs, learning_rate, batch_size, training_images, test_images, client_url):
        for training_client in self.training_clients.values():
            if training_client.client_url == client_url.strip():
                if (epochs!= 'None'): training_client.epochs = int(epochs.strip())
                if (learning_rate!= 'None'): training_client.learning_rate = float(learning_rate.strip())
                if (batch_size!= 'None'): training_client.batch_size = int(batch_size.strip())
                if (training_images!= 'None'): training_client.training_images = int(training_images.strip())
                if (test_images!= 'None'): training_client.test_images = int(test_images.strip())

    def get_list_tempos(self):

        num_of_rounds = len(self.tempos_rounds)
        res_list = [round(self.tempos_rounds[i] - ([self.tempos_rounds[0]] * num_of_rounds)[i],3) for i in range(num_of_rounds)]

        return res_list

    def get_tempos_and_accuracies(self):

        accuracies = []
        test_accuracies = []

        for training_client in self.training_clients.values():
            accuracies.append(training_client.accuracies)
            test_accuracies.append(training_client.test_accuracies)

        return self.get_list_tempos(), accuracies, test_accuracies

    def get_training_clients(self):

        training_clients = {}

        for training_client in self.training_clients.values():
            training_clients[training_client.client_url] = copy.deepcopy(training_client)
            training_clients[training_client.client_url].model_params = None #not necessary to send params...
            training_clients[training_client.client_url].status = None #not necessary to send status...
            training_clients[training_client.client_url] = training_clients[training_client.client_url].__dict__ # "serializing objects..."

        return training_clients

    def set_server_version(self, version):
        self.version = int(version.strip())