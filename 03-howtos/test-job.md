````
kubectl get -n git configmap
kubectl get configmap gitea-seed-files -n git -o yaml

kubectl delete job gitea-seed -n git
kubectl apply -f  00-environment/gitea-seed.yaml
kubectl get pod -n git

````