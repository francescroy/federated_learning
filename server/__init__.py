import asyncio
import os
from flask import json
import pickle

from flask import (
    Flask, Response, request, render_template
)

from .server import Server
from .utils import request_params_to_model_params


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    server = Server()

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'fl-network.sqlite'),
    )
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        clients_ready_for_training = server.can_do_training()
        return render_template("index.html",
                               server_status=server.status,
                               training_clients=server.training_clients,
                               clients_ready_for_training=clients_ready_for_training)

    @app.route('/training', methods=['POST'])
    def training():
        print('Request POST /training')
        training_type = request.json['training_type']
        successful_training = asyncio.run(server.start_training(training_type))
        if successful_training is True:
            return Response(status=200)
        else:
            return Response(status=500)

    @app.route('/client', methods=['POST'])
    def register_client():
        print('Request POST /client for client_url [', request.form['client_url'], ']')
        server.register_client(request.form['client_url'])
        return Response(status=201)

    @app.route('/client', methods=['DELETE'])
    def unregister_client():
        print('Request DELETE /client for client_url [', request.form['client_url'], ']')
        server.unregister_client(request.form['client_url'])
        return Response(status=200)

    @app.route('/model_params', methods=['PUT'])
    def update_weights():
        client_url = request.json['client_url']
        training_type = request.json['training_type']
        print('Request PUT /model_params for client_url [', client_url, '] and training type:', training_type)
        try:
            training_client = server.training_clients[request.json['client_url']]

            training_client.losses.append(float(request.json['loss']))
            training_client.accuracies.append(float(request.json['accuracy']))
            training_client.test_losses.append(float(request.json['test_loss']))
            training_client.test_accuracies.append(float(request.json['test_accuracy']))

            server.update_client_model_params(training_type, training_client, request_params_to_model_params(training_type, request.json))
            return Response(status=200)
        except KeyError:
            print('Client', client_url, 'is not registered in the system')
            return Response(status=401)

    @app.errorhandler(404)
    def page_not_found(error):
        return 'This page does not exist', 404

    @app.route('/set_epochs_lr_batchsize_training_test', methods=['POST'])
    def set_epochs_lr_batchsize_training_test():
        server.set_epochs_lr_batchsize_training_test(request.form['epochs'],request.form['lr'],request.form['batchsize'],request.form['training'],request.form['test'])
        return Response(status=200)

    @app.route('/set_epochs_lr_batchsize_training_test_for_client', methods=['POST'])
    def set_epochs_lr_batchsize_training_test_for_client():
        server.set_epochs_lr_batchsize_training_test_for_client(request.form['epochs'],request.form['lr'],request.form['batchsize'],request.form['training'],request.form['test'],request.form['clienturl'])
        return Response(status=200)

    @app.route('/get_tempos_and_accuracies', methods=['GET'])
    def get_tempos_and_accuracies():
        tempos, accuracies, test_accuracies = server.get_tempos_and_accuracies()
        response = app.response_class(
            response=json.dumps([tempos,accuracies,test_accuracies]),
            status=200,
            mimetype='application/json'
        )
        return response

    @app.route('/get_training_clients', methods=['GET'])
    def get_training_clients():
        training_clients = server.get_training_clients()
        response = app.response_class(
            response=json.dumps(list(training_clients.values())),
            status=200,
            mimetype='application/json'
        )
        return response

    @app.route('/set_server_version', methods=['POST'])
    def set_server_version():
        server.set_server_version(request.form['version'])
        return Response(status=200)

    return app
