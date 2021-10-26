
#!/bin/bash

# holaaaaa

valid=true
while [ $valid ]
do
  #curl -X POST -H "Content-Type: application/json" -d '{"training_type": "CHEST_X_RAY_PNEUMONIA"}' http://10.139.40.19:5000/training
  curl -X POST -H "Content-Type: application/json" -d '{"training_type": "CHEST_X_RAY_PNEUMONIA"}' http://127.0.0.1:5000/training
  sleep 2
  

done
