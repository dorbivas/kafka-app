#helm repo add bitnami https://charts.bitnami.com/bitnami
#helm repo update
helm delete my-kafka
helm dependency update kafka-cluster-chart
helm upgrade --install my-kafka bitnami/kafka -f kafka-cluster-chart/values.yaml




