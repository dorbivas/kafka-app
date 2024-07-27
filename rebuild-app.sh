#helm repo add bitnami https://charts.bitnami.com/bitnami
#helm repo update

helm delete my-kafka-app
helm upgrade --install kafka bitnami/kafka --version 29.3.13 --values kafka-config.yaml
echo "services:" 
kubectl get svc my-kafka
helm upgrade --install my-kafka-app . 


