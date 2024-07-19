helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install my-kafka bitnami/kafka --set replicaCount=3 --set zookeeper.enabled=true --set zookeeper.replicaCount=3 --set allowPlaintextListener=yes
kubectl exec -it $(kubectl get pods -l app.kubernetes.io/instance=my-kafka,app.kubernetes.io/component=kafka -o jsonpath="{.items[0].metadata.name}") -- kafka-topics.sh --create --topic test --partitions 1 --replication-factor 3 --bootstrap-server localhost:9092

