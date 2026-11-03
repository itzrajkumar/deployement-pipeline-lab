# Deployment Pipeline Lab

A learning project that uses GitHub Actions to test a small Python service and build its Docker image.

The service uses synthetic data only. It does not process real payments or use customer information.

## What the pipeline does

When code is pushed to `main` or a pull request targets `main`, GitHub Actions:

1. Checks out the project code.
2. Sets up Python.
3. Runs the health endpoint test.
4. Builds the Docker image.

## Run locally

Run the service:

```bash
python3 app.py

Open http://localhost:8000/health to check it.
Run the test in a second terminal:
"python3 -m unittest -v"
Run with Docker
Build the image:
"docker build -t deployment-pipeline-lab ."
Run the container:
"docker run --rm -p 8000:8000 deployment-pipeline-lab"
Open http://localhost:8000/health, then press Control+C to stop the container.