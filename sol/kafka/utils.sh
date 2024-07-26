
kubectl apply -f kafka-cleanup-job.yaml
kubectl apply -f role.yaml
helm upgrade --install kafka bitnami/kafka --version 29.3.13 --values kafka-config.yaml

/opt/bitnami/kafka/bin/kafka-consumer-groups.sh --bootstrap-server kafka-controller-0.kafka-controller-headless.default.svc.cluster.local:9092 --delete-offsets --group breeds_group --topic breeds_topic:0,1 
/opt/bitnami/kafka/bin/kafka-consumer-groups.sh --bootstrap-server kafka-controller-0.kafka-controller-headless.default.svc.cluster.local:9092 --delete --group breeds_group 
/opt/bitnami/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --delete --group breeds_group 
/opt/bitnami/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --reset-offsets --group breeds_group --topic breeds_topic:0,1s



/opt/bitnami/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --delete --group breeds_group 
/opt/bitnami/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --reset-offsets --group breeds_group --topic breeds_topic:0


{ "partitions": [ { "topic": "breed_topic", "partition": 0, "offset": 0 } ], "version": 1 }
/opt/bitnami/kafka/bin/kafka-delete-records.sh --bootstrap-server localhost:9092 --offset-json-file j.json