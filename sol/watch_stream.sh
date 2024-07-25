watch -d "kubectl logs $(kubectl get pods | grep producer | awk '{print $1}') | tail -f"
watch -d "kubectl logs $(kubectl get pods | grep consumer | awk '{print $1}')"

#count rec : 
watch -d "kubectl logs $(kubectl get pods | grep consumer | awk '{print $1}')| grep Received | wc -l "

