kubectl delete deployment breed-producer
kubectl delete deployment breed-consumer

kubectl apply -f producer-deployment.yaml
kubectl apply -f consumer-deployment.yaml

helm install kafka bitnami/kafka --set replicaCount=3