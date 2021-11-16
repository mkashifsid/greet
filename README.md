# Greet
Greet application is based on Python(3.6) and it requires Redis server. We will deploy this application 
and Redis server on Kubernetes, application code and Kubernetes object files are in the same repository. 
First we need to setup the Redis server, as this is the production grade application then it requires a 
redis cluster for the high availability with at least 3 nodes, from these 3 nodes one node will be master 
and other two nodes will be slaves, and if master node goes down then sentinel will come into play and 
elect a new master node from the two slaves and now this new elected node will be the new master node of 
this redis cluster.

# Sentinel
When we use redis in cluster then we also need Sentinel because sentinel checks the current master node
and then sends the write request to only master node, and if there is read request then sentinel sends
the request to slaves, this mechanism redis does not support so we have to use the sentinel. 

### Greet code changes for sentinel
I have added the python sentinel library in the code also added sentinel master
and slave endpoints for read and write.

NOTE : Assuming that the Kubernetes cluster is already setup on AWS EKS, this EKS cluster has 3 worker 
nodes and all worker nodes and EKS cluster are in the private subnet of the VPC, also Metric Server, 
and Cluster Autoscaler is installed on the EKS cluster to autoscale the deployments.

Authenticate with EKS cluster then run the below steps,
## Redis server setup
```
#create configmap for the redis server
kubectl create -f kubernetes/redis-configmap.yml

#create redis server as a statefulset
kubectl create -f kubernetes/redis-statefulset.yml
```

## Sentinel setup

```
#create sentinel as a statefulset
kubectl create -f kubernetes/sentinel-statefulset.yml
```

Now we have redis cluster and sentinel ready so we can move to application deployment.

## Greet application deployment

```
#build docker image
docker build -t greet:v1 .

#tag docker image with the username of the registry
docker tag greet:v1 kashifsiddiqui/greet:v1

#login on docker server from the server on which you created the docker image and enter the
#username and password
docker login docker.io

#push docker image to docker registry (you can change the name of the registry to your own)
docker push kashifsiddiqui/greet:v1

#create a secret for the image pulling request from the kubernetes cluster (use your own
#username, password and docker server name)
kubectl create secret docker-registry regcred --docker-server=docker.io/kashifsiddiqui
--docker-username=xxxx --docker-password=xxxx

#deploy greet deployment (change the name of the image in the deployment file
#"kubernetes/greet-deployment.yml" and use the one which we just pushed in our registry
#in previous step)
kubectl create -f kubernetes/greet-deployment.yml

#expose the deployment with the service
kubectl create -f kubernetes/greet-svc.yml

#deploy HPA for our greet deployment
kubectl create -f kubernetes/greet-hpa.yml

#deploy ingress (assuming that the ingress controller and acme.co SSL certificate secret
#are already installed on the kubernetes cluster)
kubectl create -f kubernetes/greet-ingress.yml

```

## Check the deployed application
Browse the URL https://svc7.acme.co

To change name in greeting, send a POST request

```
curl -X POST -H "Content-Type: application/json" -d "{\"name\": \"Tom\"}" https://svc7.acme.co
```
