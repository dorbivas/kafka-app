#helm repo add bitnami https://charts.bitnami.com/bitnami
#helm repo update
helm upgrade --install kafka bitnami/kafka --version 29.3.13 --values kafka-config.yaml

#kafka shells 
# /opt/bitnami/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --delete --group breeds_group 
# /opt/bitnami/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --reset-offsets --group breeds_group --topic breeds_topic:0
# json: { "partitions": [ { "topic": "breed_topic", "partition": 0, "offset": 0 } ], "version": 1 }
# /opt/bitnami/kafka/bin/kafka-delete-records.sh --bootstrap-server localhost:9092 --offset-json-file j.json