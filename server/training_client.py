from .client_training_status import ClientTrainingStatus


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

        self.init_training_time = None
        self.end_training_time = None


    def __str__(self):
        return "Training client:\n--Client URL: {}\n--Status: {}\n".format(
            self.client_url,
            self.status)
