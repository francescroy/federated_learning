
import numpy as np

def decide_number_of_images_for_next_round(training_clients):

    time_window = 10 

    time_mean = []
    workload_rythm_mean = []


    for client in training_clients.values():

        last_window_slice_init = np.array(client.init_training_time[-time_window::])
        last_window_slice_end = np.array(client.init_training_time[-time_window::])
        last_window_time = last_window_slice_end - last_window_slice_init
        print("Hereeeee: ",last_window_time)
        print(np.mean(last_window_time))
        time_mean.append(np.mean(last_window_time))


    for client in training_clients.values():

        if client.training_images is None:
            client.training_images = 400




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














