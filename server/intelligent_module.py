

def decide_number_of_images_for_next_round(training_clients):

    # Tots comencen amb el mateix numero de imatges: 200
    # Fem les mitges dels teus ultims work / seconds...

    for client in training_clients.values():

        if client.training_images is None:
            client.training_images = 200
        if client.test_images is None:
            client.test_images = 100

        workload_rythm = float(client.training_images / (client.end_training_time - client.init_training_time))
        print("\n\n\n\n\n\n\n\nHereeeee: ",workload_rythm,"\n\n\n\n\n\n\n\n")

        if workload_rythm > 6:
            client.training_images = client.training_images + 10
            client.test_images = client.test_images + 5

            if client.training_images > 1000 or client.test_images > 500:
                client.training_images = 1000
                client.test_images = 500

        elif workload_rythm < 2:
            client.training_images = int(client.training_images/2)
            client.test_images = int(client.test_images / 2)

            if client.training_images < 200 or client.test_images < 100:
                client.training_images = 200
                client.test_images = 100

    return














