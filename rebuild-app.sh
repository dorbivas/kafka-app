#helm repo add bitnami https://charts.bitnami.com/bitnami
#helm repo update

# helm install my-kafka bitnami/kafka --set replicaCount=3 --set zookeeper.enabled=true --set zookeeper.replicaCount=3 --set allowPlaintextListener=yes
#helm install my-kafka bitnami/kafka --set replicaCount=3 --set zookeeper.replicaCount=3 --set global.storageClass=standard --set persistence.enabled=false

helm delete my-kafka-app
helm upgrade --install my-kafka bitnami/kafka -f my-kafka-app/values.yaml
helm upgrade --install my-kafka-app my-kafka-app
echo "services:" 
kubectl get svc my-kafka
echo "ep:"
kubectl get ep my-kafka
sleep 5
kubectl logs -f $(kubectl get pods -l app.kubernetes.io/name=kafka -o jsonpath="{.items[0].metadata.name}")



