

def decide_number_of_images_for_next_round(training_clients):

    time_window = 5

    worst_client = list(training_clients.values())[0]

    for client in training_clients.values():
        if client.get_mean_workload_rythm(time_window) < worst_client.get_mean_workload_rythm(time_window):
            worst_client= client

    #print(worst_client.get_mean_workload_rythm(time_window))

    for client in training_clients.values():
        if client.training_images is None:
            client.training_images = 400

    for client in training_clients.values():
        if client.client_url != worst_client.client_url:
            #if client.get_mean_training_time(time_window) < worst_client.get_mean_training_time(time_window):
            if client.get_last_training_time() < worst_client.get_last_training_time():
                client.training_images = client.training_images + 10





    """
        workload_rythm = float(client.training_images / (client.end_training_time - client.init_training_time))
        print("\n\n\n\n\n\n\n\nHereeeee: ",workload_rythm,"\n\n\n\n\n\n\n\n")

        if workload_rythm > 6.25:
            client.training_images = client.training_images + 10

            if client.training_images > 1000:
                client.training_images = 1000

        elif workload_rythm < 4.80:
            client.training_images = int(client.training_images/2)

            if client.training_images < 400:
                client.training_images = 400
                
    """

    return














