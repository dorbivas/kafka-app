helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# helm install my-kafka bitnami/kafka --set replicaCount=3 --set zookeeper.enabled=true --set zookeeper.replicaCount=3 --set allowPlaintextListener=yes
#helm install my-kafka bitnami/kafka --set replicaCount=3 --set zookeeper.replicaCount=3 --set global.storageClass=standard --set persistence.enabled=false

helm upgrade --install my-kafka bitnami/kafka -f values.yaml




