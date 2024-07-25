kubectl delete deployment breed-producer
kubectl delete deployment breed-consumer

kubectl apply -f producer-deployment.yaml
kubectl apply -f consumer-deployment.yaml

helm install kafka bitnami/kafka --set replicaCount=3

helm install kafka-release bitnami/kafka --set persistence.size=8Gi,logPersistence.size=8Gi,replicaCount=3,volumePermissions.enabled=true,persistence.enabled=true,logPersistence.enabled=true,auth.clientProtocol=plaintext,allowPlaintextListener=true,listeners=PLAINTEXT://0.0.0.0:9092,advertisedListeners=PLAINTEXT://:9092,listenerSecurityProtocolMap=PLAINTEXT:PLAINTEXT,interBrokerListenerName="PLAINTEXT",serviceAccount.create=true,rbac.create=true,image.tag=latest
helm upgrade kafka-release bitnami/kafka --set externalAccess.enabled=true