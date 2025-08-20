Deploy Happy Vibe DevOps App with Tekton CI/CD

  Objective

  Create and execute a complete Tekton CI/CD pipeline that:
  1. Fetches source code from the local Git repository
  2. Builds and pushes a container image
  3. Deploys the Flask application to Kubernetes
  4. Verifies successful deployment

  Task Requirements

  Source Repository

  - Git URL: http://host.docker.internal:3000/gitea-admin/seed-repo.git (REQUIRED - source code must be checked out from this URL)
  - Required files: app.py, Dockerfile, deployment.yaml
  - Application: Flask app serving "Happy Vibe Code DevOps! 😃" on port 80

  Container Build Configuration

  - Local registry: localhost:5001 (for builds and pushes)
  - Kind registry: host.docker.internal:5001 (for cluster pulls)
  - Image tag: vibedevops:latest
  - Build tool: [buidalh](https://buildah.io/)

  Kubernetes Deployment Target

  - Namespace: happy-vibe-devops
  - Service ports: ClusterIP 8080, NodePort 30080
  - Resource limits: 128Mi memory, 100m CPU
  - Image source: host.docker.internal:5001/vibedevops:latest

  Implementation Steps

  1. Generate Tekton Resources

  Create these files in the tekton/ directory:
  - workspace-pvc.yaml - Shared workspace for pipeline tasks
  - task-fetch-source.yaml - Git clone task (must use http://host.docker.internal:3000/gitea-admin/seed-repo.git)
  - task-build-push.yaml - Image build and push task
  - task-deploy.yaml - Kubernetes deployment task
  - pipeline.yaml - Pipeline orchestration
  - pipelinerun.yaml - Pipeline execution trigger

  2. Deploy and Execute Pipeline

  # Apply all Tekton resources
  kubectl apply -f tekton/

  # Execute pipeline
  kubectl apply -f tekton/pipelinerun.yaml

  # Monitor execution (use MCP server if available)
  kubectl get pipelinerun -n happy-vibe-devops -w

  3. Verify Deployment

  # Check deployment status
  kubectl get all -n happy-vibe-devops

  # Test application
  kubectl port-forward -n happy-vibe-devops svc/vibedevops-service 8080:8080 &
  curl localhost:8080 | grep -i "happy vibe.*devops"

  Execution Requirements

  - Must execute: Apply all manifests and run the pipeline
  - Must verify: Pipeline completes successfully with all tasks passing
  - Must validate: Application is accessible and serves expected content
  - Must demonstrate: Show pipeline logs and final deployment status

  Technical Specifications

  - Source code must be fetched from: http://host.docker.internal:3000/gitea-admin/seed-repo.git
  - Use insecure registry configuration for local development
  - Include proper error handling and retry logic in tasks
  - Ensure compatibility with Kind cluster and local registry setup
  - Configure proper RBAC permissions for pipeline execution

  Success Criteria

  ✅ All Tekton resources deploy without errors✅ Pipeline executes end-to-end successfully✅ Application serves "Happy Vibe DevOps! 😃" content✅ Service is accessible on both ClusterIP and NodePort✅
  Pipeline logs show successful completion of all tasks