# Deployment Pipeline Lab

A beginner DevOps learning project that uses GitHub Actions to test a small Python service, build a Docker image, and publish it to GitHub Container Registry (GHCR).

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

## Project structure

```text
deployment-pipeline-lab/
├── .github/
│   └── workflows/
│       └── ci.yml
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
5. On pushes to `main`, publishes the image to GHCR.

Pull requests run the test and build steps, but do not publish an image.

The published image supports both `linux/amd64` and `linux/arm64`. Docker selects the suitable version for the computer that downloads it.

## Requirements

- Python 3
- Docker Desktop
- Git
- A GitHub account

The service and test use Python's standard library; no additional Python packages are required.

## Run locally

Start the service:

```bash
python3 app.py
```

Open <http://localhost:8000/health>. You should see the JSON health response shown above.

Stop the service by returning to the terminal and pressing **Control+C**.

### Run the automated test

Make sure the manually started service is stopped, then run:

```bash
python3 -m unittest -v
```

The test starts the service, requests `/health`, and checks the response.

## Build and run with Docker

Build the image from the project folder:

```bash
docker build -t deployment-pipeline-lab .
```

Start a container:

```bash
docker run --rm -p 8000:8000 --name deployment-pipeline-lab deployment-pipeline-lab
```

Open <http://localhost:8000/health> to check it. Stop the container with **Control+C**.

## Pull and run the image from GHCR

The workflow publishes these tags:

- `latest` points to the most recently published image.
- `sha-<commit-id>` identifies the exact commit used to build an image.

The package is private. To download it from a Mac, authenticate Docker to GHCR with a GitHub personal access token (classic) that has the `read:packages` scope. Keep the token private; never put it in this repository or share it. GitHub documents this authentication method for private container packages. [GHCR authentication documentation](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)

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

Open <http://localhost:8000/health> to check it. Stop the container with **Control+C**.

The workflow uses GitHub's automatically created `GITHUB_TOKEN` to publish the image; no personal token is stored in the workflow. [GitHub Actions package publishing guide](https://docs.github.com/en/actions/tutorials/publish-packages/publish-docker-images)

## Current scope

This project automates testing and image building, publishes a multi-platform image to GHCR, and verifies that the published image runs locally.

It does not deploy the service to a cloud environment yet. Cloud deployment can be added as a later learning stage.

## Limitations

- The service only provides a health endpoint; it does not implement payment processing.
- This is a learning project and is not designed for production use.
- The GHCR package is private and requires authentication to download.