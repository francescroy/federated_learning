from os import environ

DEFAULT_SERVER_URL = 'http://127.0.0.1:5000'
GLOBAL_TMP_PATH = '/tmp'
GLOBAL_DATASETS = '/home/francesc/Escritorio/folder_client' # inside there is chest_xray folder
if environ.get('CLIENT_URL') == "http://localhost:5002":
    GLOBAL_DATASETS = '/home/francesc/Escritorio/datasets' # inside there is chest_xray folder
INITIAL_MODEL_PATH = '/home/francesc/Escritorio/folder_client/keras_model'