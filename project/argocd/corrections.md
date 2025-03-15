## ArgoCD UI login credentials
- username: admin
- password: kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode

## Fix CoreDNS to work with a Mac
1. Edit CoreDNS-configuration:  
kubectl -n kube-system edit cm coredns
2. Replace:  
forward . /etc/resolv.conf  
with:  
forward . 8.8.8.8 8.8.4.4  
3. Restart CoreDNS:  
kubectl -n kube-system rollout restart deployment coredns  

Now CoreDNS uses an external DNS (the DNS from Google) 