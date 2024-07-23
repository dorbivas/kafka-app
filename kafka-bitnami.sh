#helm repo add bitnami https://charts.bitnami.com/bitnami
#helm repo update
helm delete my-kafka
helm dependency update kafka-cluster-chart
helm upgrade --install my-kafka kafka-cluster-chart --values kafka-cluster-chart/values.yaml




