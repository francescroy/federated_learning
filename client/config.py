from os import environ

DEFAULT_SERVER_URL = 'http://127.0.0.1:5000'
GLOBAL_TMP_PATH = None
GLOBAL_DATASETS = None # inside there is chest_xray folder
if environ.get('CLIENT_URL') == "http://localhost:5001":
    print("I'm client 1")
    GLOBAL_TMP_PATH = '/tmp'
    GLOBAL_DATASETS = '/home/francesc/Escritorio/folder_client' # inside there is chest_xray folder
if environ.get('CLIENT_URL') == "http://localhost:5002":
    print("I'm client 2")
    GLOBAL_TMP_PATH = '/tmp2'
    GLOBAL_DATASETS = '/home/francesc/Escritorio/folder_client_2' # inside there is chest_xray folder
if environ.get('CLIENT_URL') == "http://localhost:5003":
    print("I'm client 3")
    GLOBAL_TMP_PATH = '/tmp3'
    GLOBAL_DATASETS = '/home/francesc/Escritorio/folder_client_3' # inside there is chest_xray folder
