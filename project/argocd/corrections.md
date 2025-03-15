## ArgoCD UI login credentials
- username: admin
- password: kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode

