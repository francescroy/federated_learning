
import requests
import time



url = 'http://127.0.0.1:5000'
#url = 'http://10.139.40.19:5000'

n=0

while n< 5:

#use the 'headers' parameter to set the HTTP headers:
    x = requests.post(url+"/training", json = {'training_type': 'CHEST_X_RAY_PNEUMONIA'}, headers = {"Content-Type": "application/json"})
    n = n+1
    time.sleep(2.4)


x = requests.get(url+"/get_tempos_and_accuracies")
print(x.text)



#curl -X GET http://127.0.0.1:5000/get_tempos_and_accuracies


