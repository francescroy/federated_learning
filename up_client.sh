

export CLIENT_URL='http://localhost:5001'
flask run --port 5001


#!/bin/bash
# else example
#if [ $1 -eq 1 ]
#then
#    sudo docker run --rm --name fl-client-5001 -e CLIENT_URL='http://172.17.0.3:5000' -e SERVER_URL='http://172.17.0.2:5000' fl-client:latest
#else
#    sudo docker run --rm --name fl-client-5002 -e CLIENT_URL='http://172.17.0.4:5000' -e SERVER_URL='http://172.17.0.2:5000' fl-client:latest
#fi


#sudo docker run --rm --name fl-client-5001 -e CLIENT_URL='http://172.17.0.3:5000' -e SERVER_URL='http://172.17.0.2:5000' fl-client:latest


#sudo docker run --rm --name fl-client-5002 -e CLIENT_URL='http://172.17.0.4:5000' -e SERVER_URL='http://172.17.0.2:5000' fl-client:latest
