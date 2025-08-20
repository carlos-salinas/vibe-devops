
# Prerequisities 

* Podman Runtime and CLI
* Kind
* Kubectl 
* Claude Code CLI

# Configurate the environment

Allow the unsecure local registry by appending the following snippet at the registries.conf of the Podman VM:

```
[[registry]]
location = "localhost:5001"
insecure = true
```

```
podman machine ssh --username root <podman-machine-name>
vi /etc/containers/registries.conf
```

Instanciate Kubernetes in Docker with the proper configuration

```
kind create cluster --name claude-tekton --config  00-environment/kind-config.yaml
```

Install Tekton

````
kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
```


Instanciate a local registry
```
podman rm -f registry || true 
podman run -d --restart=always -p 5001:5000 --name registry registry:latest
```


Install a local git server

```
helm repo add gitea-charts https://dl.gitea.io/charts/
helm repo update

helm install gitea gitea-charts/gitea \
  --namespace git --create-namespace \
  --values 00-environment/gitea-values.yaml
```

Seed the Gitea server with a sample repository

```
kubectl create configmap gitea-seed-files \
  --from-file=app.py=01-app/app.py \
  --from-file=Dockerfile=01-app/Dockerfile \
  --from-file=deployment.yaml=01-app/deployment.yaml \
  -n git
  
kubectl apply -f  00-environment/gitea-seed.yaml
```

Watch Gitea logs

```
kubectl -n git logs job/gitea-seed -f
```

Verify repository creation

```
git ls-remote http://localhost:3000/gitea-admin/test-repo.git
```

# Test configuration

Pull an sample image

```
podman pull nginx:alpine
podman tag nginx:alpine localhost:5001/nginx:alpine
podman push localhost:5001/nginx:alpine

```

Deploy in Kubernetes

```
kubectl apply -f 00-environment/deployment.yaml
```

Verify the deployment pod is running

````
kubectl get all 
````


kubectl create ns happy-vibe-devops
namespace/happy-vibe-devops created


# Reference

* [Configure image registries](https://podman-desktop.io/docs/containers/registries)
* [Claude Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)

# Tools

* [Asciinema Terminal recording](https://asciinema.org/)
* [Tmux Terminal Multiplexer](https://github.com/tmux/tmux/wiki)
* [Iterm2 - Mac Terminal Emulator](https://iterm2.com/)

