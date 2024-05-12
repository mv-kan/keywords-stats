# Keyword Statistics

This application is designed to count occurrences of specific keywords: `["checkpoint", "avanan", "email", "security"]`. Additionally, it provides statistical insights based on these counts.

## How to run? 

### 1. Docker Compose (Recommended)
Prerequisite
1. docker 
```
docker compose up 
```
Once the application is up, you can access it at http://localhost/redoc.

### 2. Kubernetes (with Horizontal Pod Autoscaler)
Prerequisite
- kubectl
- minikube
- docker 
```
# set up minikube
minikube start 
# you may want to enable metrics-server
minikube addons enable metrics-server
minikube dashboard
```

Deploy the application using:

```
kubectl apply -f ./k8s-deployment
```

Use a load generator to observe pod autoscaling:
```
kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while sleep 0.001; do wget -q -O- http://keystat-app/api/v1/stats; done"
```

Watch container CPU load:
```
kubectl get hpa keystat-app-hpa --watch
```

Access the application:
```
# This command will display the IP address of the hosted application.
minikube service keystat-app
```

## Example

In bash terminal:
```
curl -X POST 'http://localhost/api/v1/events' -d 'a lot of security stuff is handled by very smart people'
curl -X POST 'http://localhost/api/v1/events' -d 'the email is very secure'
# this will return counted keywords in last 60 seconds 
curl 'http://localhost/api/v1/stats?interval=60' 
```

## Pytest and Unit Tests

Prerequisite
1. Poetry ([How To Install Poetry](https://python-poetry.org/docs/))
2. Docker

```
# Install all needed dependencies
poetry install
# Run docker-compose for the Redis container: 
docker compose up 
# Then, run the tests
poetry run pytest
```