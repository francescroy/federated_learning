from .client_training_status import ClientTrainingStatus
import numpy as np

class TrainingClient:
    def __init__(self, client_url):
        self.client_url = client_url
        self.status = ClientTrainingStatus.IDLE

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


    def __str__(self):
        return "Training client:\n--Client URL: {}\n--Status: {}\n".format(
            self.client_url,
            self.status)

    def add_workload_rythm(self, default_training_images, round):
        rythm = None

        if self.training_images is None:
            rythm = float(2*default_training_images / (self.end_training_time[round-1] - self.init_training_time[round-1]))
        else:
            rythm = float(2*self.training_images / (self.end_training_time[round-1] - self.init_training_time[round-1]))

        self.workload_rythm.append(rythm)

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