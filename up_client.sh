

#export CLIENT_URL='http://localhost:5001'
#flask run --port 5001

sudo docker run --rm --name fl-client -p 5000:5000 -e CLIENT_URL='http://10.228.207.201:5000' -e SERVER_URL='http://10.139.40.19:5000' -v /home/francesc/Escritorio/folder_client:/federated-learning-network/datasets_and_model fl-client:latest
