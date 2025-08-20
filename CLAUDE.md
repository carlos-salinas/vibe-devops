# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a DevOps repository focused on Kubernetes development and deployment tooling using Kind (Kubernetes in Docker), local container registries, and Tekton pipelines. The project demonstrates a complete CI/CD workflow for deploying a Flask-based web application that generates static HTML content served via Nginx.

## Architecture

### Container Registry Architecture
- **Local Registry**: `host.docker.internal:5001` (for Kind cluster access) / `localhost:5001` (for local development)
- **Insecure Registry**: Configured for local development without TLS
- **Podman Integration**: Uses Podman as the primary container runtime instead of Docker

### Core Components
- **01-app/**: Flask application and Kubernetes manifests
  - `app.py`: Flask app that generates static HTML with "Happy Vibe DevOps" content
  - `Dockerfile`: Multi-stage build with Python builder and Nginx runtime
  - `deployment.yaml`: Kubernetes Deployment and Service for the web app
  - `namespace.yaml`: Creates the `happy-vibe-devops` namespace
- **00-environment/**: Environment and cluster configuration
  - `kind-config.yaml`: Kind cluster config with local registry support
  - `deployment.yaml`: Test deployment for registry validation
- **tekton/**: Complete Tekton CI/CD pipeline
  - `pipeline.yaml`: Main pipeline orchestrating build and deploy tasks
  - `task-*`: Individual tasks for source fetch, build/push, and deployment
  - `workspace-pvc.yaml`: Persistent volume claim for pipeline workspace
  - `pipelinerun.yaml`: Pipeline execution configuration
- **02-prompts/**: Project specifications for AI-generated deployments
- **03-howtos/**: Terminal recording documentation

### Multi-Stage Docker Build
The application uses a multi-stage Dockerfile:
1. **Builder stage**: Python 3.11 Alpine with Flask to generate static HTML
2. **Runtime stage**: Nginx Alpine serving the generated static content

## Common Development Commands

### Environment Setup (Podman-based)
```bash
# Configure Podman VM for insecure local registry
podman machine ssh --username root <podman-machine-name>
# Edit /etc/containers/registries.conf to add localhost:5001 as insecure
# Add this snippet:
# [[registry]]
# location = "localhost:5001"
# insecure = true

# Create Kind cluster with local registry support
kind create cluster --name claude-tekton --config 00-environment/kind-config.yaml

# Start local container registry (remove existing if present)
podman rm -f registry || true 
podman run -d --restart=always -p 5001:5000 --name registry registry:latest

# Install Tekton in cluster
kubectl apply -f https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
```

### Optional: Local Git Server Setup
```bash
# Install Gitea for local Git repository hosting
helm repo add gitea-charts https://dl.gitea.io/charts/
helm repo update

helm install gitea gitea-charts/gitea \
  --namespace git --create-namespace \
  --values 00-environment/gitea-values.yaml

# Seed Gitea with sample repository
kubectl create configmap gitea-seed-files \
  --from-file=app.py=01-app/app.py \
  --from-file=Dockerfile=01-app/Dockerfile \
  --from-file=deployment.yaml=01-app/deployment.yaml \
  -n git
  
kubectl apply -f 00-environment/gitea-seed.yaml

# Watch seeding process
kubectl -n git logs job/gitea-seed -f

# Verify repository creation
git ls-remote http://localhost:3000/gitea-admin/test-repo.git
```

### Manual Build and Deploy Workflow
```bash
# Build and push image manually (from repository root)
podman build -t localhost:5001/vibedevops:latest -f 01-app/Dockerfile 01-app/
podman push localhost:5001/vibedevops:latest

# Create namespace and deploy application
kubectl apply -f 01-app/namespace.yaml
kubectl apply -f 01-app/deployment.yaml

# Verify deployment
kubectl get all -n happy-vibe-devops
kubectl port-forward -n happy-vibe-devops svc/vibedevops-service 8080:8080

# Alternative: Create namespace manually if needed
kubectl create ns happy-vibe-devops
```

### Tekton Pipeline Workflow
```bash
# Deploy pipeline resources (Tekton must be installed first)
kubectl apply -f tekton/workspace-pvc.yaml
kubectl apply -f tekton/task-fetch-source.yaml
kubectl apply -f tekton/task-build-push.yaml
kubectl apply -f tekton/task-deploy.yaml
kubectl apply -f tekton/pipeline.yaml

# Execute pipeline
kubectl apply -f tekton/pipelinerun.yaml

# Monitor pipeline execution
kubectl get pipelinerun -n happy-vibe-devops
kubectl logs -f pipelinerun/<run-name> -n happy-vibe-devops
```

### Verification Commands
```bash
# Test application endpoint
kubectl port-forward -n happy-vibe-devops svc/vibedevops-service 8080:8080
curl localhost:8080 | grep "Happy Vibe.*DevOps"

# Check NodePort access (if Kind port mapping configured)
curl localhost:30080

# Test local registry connectivity
podman pull nginx:alpine
podman tag nginx:alpine localhost:5001/nginx:alpine
podman push localhost:5001/nginx:alpine
kubectl apply -f 00-environment/deployment.yaml
```

## Key Configuration Details

### Kind Cluster Configuration
- Registry mirror: `host.docker.internal:5001`
- Insecure TLS skip verification enabled
- Empty authentication for local registry access
- Containerd runtime with custom registry patches for local development

### Application Architecture
- **Flask Backend**: Generates static HTML with CSS animations
- **Nginx Frontend**: Serves static content on port 80
- **Kubernetes Service**: NodePort on 30080, ClusterIP on 8080
- **Resource Limits**: 128Mi memory, 100m CPU limits with 64Mi/50m requests

### Tekton Pipeline Architecture
- **Source Management**: Git-based source fetching task
- **Build System**: Kaniko for container image building without Docker daemon
- **Registry Integration**: Pushes to local insecure registry
- **Deployment**: Automated Kubernetes manifest application
- **Workspace**: Shared PVC for pipeline data persistence

### Tekton MCP Server Integration

The project supports integration with the [Tekton MCP Server](https://github.com/tektoncd/mcp-server) to enable Claude Code to interact directly with Tekton resources through the Model Context Protocol.

#### MCP Server Capabilities
The Tekton MCP Server provides 10 tools for managing Tekton resources:
- **Pipeline Management**: `list_pipelines`, `start_pipeline`
- **PipelineRun Operations**: `list_pipeline_runs`, `restart_pipelinerun`
- **Task Management**: `list_tasks`, `start_task`, `list_task_runs`, `restart_taskrun`
- **Additional Features**: `list_stepactions`, `get_taskrun_logs`

#### Local MCP Server Setup
```bash
# Build and run the Tekton MCP Server locally
cd /Users/csalinas/Developer/RH/tekton-mcp-server
go build -o tekton-mcp-server cmd/tekton-mcp-server/main.go

# Run with HTTP transport (recommended for Claude Code)
./tekton-mcp-server -transport http -address :3000

# Alternative: Run with stdio transport
./tekton-mcp-server -transport stdio
```

#### Claude Code MCP Configuration
```bash
# Add Tekton MCP Server to Claude Code (HTTP transport)
claude mcp add --transport http tekton http://localhost:3000

# Add Tekton MCP Server to Claude Code (stdio transport)
claude mcp add tekton -- /path/to/tekton-mcp-server -transport stdio

# List configured MCP servers
claude mcp list

# Remove MCP server if needed
claude mcp remove tekton
```

#### Kubernetes Deployment (Optional)
```bash
# Deploy MCP Server to cluster for remote access
kubectl apply -f /Users/csalinas/Developer/RH/tekton-mcp-server/config/

# This creates:
# - tekton-mcp namespace
# - ServiceAccount with appropriate RBAC
# - Deployment running on port 8080
# - Service exposing the MCP server
```

#### Usage Examples with Claude Code
Once configured, Claude Code can interact with Tekton resources:
```bash
# Examples of what Claude Code can do with the MCP server:
# - List all pipelines in happy-vibe-devops namespace
# - Start the vibedevops-pipeline
# - Monitor pipeline run status and logs
# - Restart failed pipeline runs
# - List and manage individual tasks and task runs
```

### Terminal Recording Setup
```bash
# Create tmux session for demos
tmux new -s claude-tekton-demo
tmux Ctrl+B and %  # Split screen vertically
tmux Ctrl+B and d  # Detach session

# Record with asciinema
asciinema rec -c "tmux attach -t claude-tekton-demo"
```

## Prerequisites

Essential tools required for this project:
- **Podman Runtime and CLI**: Container management
- **Kind**: Kubernetes in Docker for local clusters
- **Kubectl**: Kubernetes command-line interface
- **Claude Code CLI**: AI-powered development assistant
- **Helm**: Kubernetes package manager (for optional Gitea setup)

## References and Tools

- [Configure image registries](https://podman-desktop.io/docs/containers/registries)
- [Claude Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Asciinema Terminal recording](https://asciinema.org/)
- [Tmux Terminal Multiplexer](https://github.com/tmux/tmux/wiki)
- [iTerm2 - Mac Terminal Emulator](https://iterm2.com/)