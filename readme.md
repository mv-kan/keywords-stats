# Keywords Stats 

redis + python fastapi microservice + pytest + poetry

tech stack:
docker, kubectl, minikube, poetry

This is application that counts these `["checkpoint", "avanan", "email", "security"]` keywords. Also you can get some statistics about it. 

## How to run? 

### 1. docker compose (recommended)
```
docker compose up 
```
and then you can visit `http://localhost/redoc`

### 2. k8s (with horizontal pod autoscaler)
```
# set up minikube and show statistics 
minikube start 
minikube dashboard
```

And then deploy everything using this command
```
kubectl apply -f ./k8s-deployment
```

Load generator to check autoscaling of pods 
```
kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://keystat-app/stats; done"
```

You can watch containers cpu load using this 
```
kubectl get hpa keystat-app-hpa --watch
```

You can access app after this command 
```
minikube service keystat-app
```
it will print out ip address of hosted application

## Example input

in terminal
```
curl -X POST 'http://localhost/api/v1/events' -d 'a lot of security stuff is handled by very smart people'
curl -X POST 'http://localhost/api/v1/events' -d 'the email is very secure'
curl 'http://localhost/api/v1/stats?interval=60' # this will return counted keywords in last 60 seconds 
```

## pytest and unit tests 

Prerequisite
```
# 1. poetry install to initialize virtual env 
poetry install
# 2. activate scripts 
source ./.venv/bin/activate
```

You should run docker-compose for redis container 
```
docker compose up 
# then you can try to run test
pytest
```

# TODO 
1. unit test for fastapi 
2. redis persistance for k8s and docker-compose 
3. redis time series +