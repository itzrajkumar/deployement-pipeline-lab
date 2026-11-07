# Deployment Pipeline Lab

A learning project that tests a small Python service, builds a Docker image, publishes it to GitHub Container Registry (GHCR), and runs it in a local Kubernetes cluster.

This is a learning demo only. It does not connect to financial systems, process real payments, or use customer data.

## What the service does

- Provides a health endpoint at `GET /health`
- Returns a JSON response showing that the service is running
- Returns `404 Not Found` for other paths

Example health response:

```json
{
  "status": "ok",
  "service": "deployment-pipeline-lab"
}
```
- Provides a version endpoint at `GET /version`
- Returns the app version, which defaults to `1.0.0` or can be set with the `APP_VERSION` environment variable

{
  "service": "deployment-pipeline-lab",
  "version": "1.0.0"
}


## Project structure

```text
deployment-pipeline-lab/
├── .github/
│   └── workflows/
│       └── ci.yml
├── k8s/
│   └── app.yaml
├── .gitignore
├── app.py
├── Dockerfile
├── README.md
└── test_app.py
```

## What the pipeline does

The GitHub Actions workflow runs when code is pushed to `main` or when a pull request targets `main`.

It:

1. Checks out the project code.
2. Sets up Python.
3. Runs the automated health endpoint test.
4. Builds the Docker image.
5. Publishes the image to GHCR when code is pushed to `main`.

Pull requests run the test and build steps, but do not publish an image.

The published image supports both `linux/amd64` and `linux/arm64`. Docker selects a suitable version for the computer downloading it.

The workflow uses GitHub's automatically created `GITHUB_TOKEN` to publish the image. It does not store a personal access token in the workflow. See [GitHub's guide to publishing Docker images](https://docs.github.com/en/actions/tutorials/publish-packages/publish-docker-images).

## Requirements

For local development and Docker:

- Python 3
- Docker Desktop
- Git
- A GitHub account

For the local Kubernetes section:

- Docker Desktop running on your Mac
- Homebrew
- kind
- kubectl

The service and tests use Python's standard library; no extra Python packages are needed.

## Run locally

Start the service:

```bash
python3 app.py
```

Open [http://localhost:8000/health](http://localhost:8000/health). You should see the JSON health response shown above.

Stop the service by returning to the terminal and pressing **Control+C**.

### Run the automated test

From the project directory, run:

```bash
python3 -m unittest -v
```

The test starts the service inside the test process on a temporary available port, requests `/health`, checks the response, and shuts the test server down. It does not require port 8000 to be free.

## Build and run with Docker

Build the image from the project directory:

```bash
docker build -t deployment-pipeline-lab:latest .
```

Start a container:

```bash
docker run --rm -p 8000:8000 --name deployment-pipeline-lab deployment-pipeline-lab:latest
```

Open [http://localhost:8000/health](http://localhost:8000/health) to check it. Stop the container with **Control+C**.

If port 8000 is already in use, you can map a different Mac port:

```bash
docker run --rm -p 8001:8000 --name deployment-pipeline-lab deployment-pipeline-lab:latest
```

Then open [http://localhost:8001/health](http://localhost:8001/health).

## Pull and run the image from GHCR

The workflow publishes image tags to GHCR:

- `latest` points to the most recently published image.
- `sha-<commit-id>` identifies an image built from a specific commit.

The package is private. To download it, authenticate Docker to GHCR using a GitHub personal access token (classic) with the `read:packages` permission. Keep the token private. Never put it in this repository or share it. See [GitHub's Container registry documentation](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry).

Sign Docker in to GHCR:

```bash
docker login ghcr.io -u YOUR_GITHUB_USERNAME
```

At the password prompt, paste the token. The token characters will not appear in the terminal.

Replace `OWNER/IMAGE` below with the exact image path shown on the GitHub package page:

```bash
docker pull ghcr.io/OWNER/IMAGE:latest
```

Run the published image:

```bash
docker run --rm -p 8000:8000 ghcr.io/OWNER/IMAGE:latest
```

Open [http://localhost:8000/health](http://localhost:8000/health) to check it. Stop the container with **Control+C**.

## Local Kubernetes deployment

The project can also run in a local Kubernetes cluster using kind. kind runs the cluster using Docker containers on your Mac. This setup does not deploy to a cloud provider or require a cloud account.

### Install the tools

Install kind and kubectl with Homebrew:

```bash
brew install kind kubectl
```

Make sure Docker Desktop is open and running.

### Build the image and create a cluster

From the project directory, build the image:

```bash
docker build -t deployment-pipeline-lab:latest .
```

Create the local cluster:

```bash
kind create cluster --name deployment-lab --wait 60s
```

This command is needed the first time you create the cluster. If the `deployment-lab` cluster already exists, you can skip this step.

Load the image into kind so the cluster can use the image built on your Mac:

```bash
kind load docker-image deployment-pipeline-lab:latest --name deployment-lab
```

Apply the Kubernetes configuration:

```bash
kubectl apply -f k8s/app.yaml
```

Check the Deployment, Pods, and Service:

```bash
kubectl get deployment,pods,service
```

The Deployment requests two app Pods. Readiness and liveness probes check the `/health` endpoint.

### Check the Kubernetes health endpoint

Start port forwarding:

```bash
kubectl port-forward service/deployment-pipeline-lab 8080:80
```

Leave that terminal running. In another terminal, check the response:

```bash
curl http://localhost:8080/health
```

You can also open [http://localhost:8080/health](http://localhost:8080/health) in a browser. The endpoint displays JSON, not an HTML website.

Press **Control+C** in the port-forward terminal when finished.

### Practice recovery

Kubernetes maintains the number of app copies specified by the Deployment. To see it replace a Pod:

1. List the Pods:

   ```bash
   kubectl get pods
   ```

2. Delete one Pod by replacing `<pod-name>` with one of the names shown:

   ```bash
   kubectl delete pod <pod-name>
   ```

3. List the Pods again:

   ```bash
   kubectl get pods
   ```

Kubernetes should create a replacement Pod so that two app Pods are running again.

### Practice scaling

Scale the app to three Pods:

```bash
kubectl scale deployment deployment-pipeline-lab --replicas=3
kubectl get pods
```

Return it to the two replicas declared in `k8s/app.yaml`:

```bash
kubectl scale deployment deployment-pipeline-lab --replicas=2
kubectl get pods
```

The scale command changes the running Deployment. The saved `k8s/app.yaml` remains the configuration to apply from the project.

### Clean up the local Kubernetes setup

Remove the app resources:

```bash
kubectl delete -f k8s/app.yaml
```

Delete the local cluster when you no longer need it:

```bash
kind delete cluster --name deployment-lab
```

Deleting the cluster removes its Kubernetes resources and containers. The Docker image built on your Mac remains available until you remove it separately.

## Current scope

This project demonstrates:

- Automated testing with GitHub Actions
- Building and publishing a multi-platform Docker image
- Running a container locally
- Deploying the app to a local Kubernetes cluster
- Checking app health with Kubernetes probes
- Replacing a deleted Pod
- Scaling the app up and down

It does not deploy the service to a cloud environment.

## Limitations

- The service only provides a health endpoint; it does not implement payment processing.
- This is a learning project and is not designed for production use.
- The GHCR package is private and requires authentication to download.
- The Kubernetes cluster runs locally on the Mac and uses local computer resources.

### Practice a rollout and rollback

Build and load a new image:

```bash
docker build -t deployment-pipeline-lab:v2 .
kind load docker-image deployment-pipeline-lab:v2 --name deployment-lab

Tell Kubernetes to use the new image and wait for the update to finish:
kubectl set image deployment/deployment-pipeline-lab app=deployment-pipeline-lab:v2
kubectl rollout status deployment/deployment-pipeline-lab
Check the new endpoint through the port-forward:
curl http://localhost:8080/version
Roll back to the previous Deployment revision:
kubectl rollout undo deployment/deployment-pipeline-lab
kubectl rollout status deployment/deployment-pipeline-lab
Check the active image and endpoints after the rollback:
kubectl get deployment deployment-pipeline-lab -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'
curl http://localhost:8080/health
In this exercise, the earlier latest image did not include /version, so that endpoint returned 404 after rollback while /health continued to respond.