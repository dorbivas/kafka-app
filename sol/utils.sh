watch -d "kubectl logs $(kubectl get pods | grep producer | awk '{print $1}')"
watch -d "kubectl logs $(kubectl get pods | grep consumer | awk '{print $1}')"

#count rec : 
watch -d "kubectl logs $(kubectl get pods | grep consumer | awk '{print $1}')| grep Received | wc -l "

