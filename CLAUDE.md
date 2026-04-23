# Hello World TypeScript Express API

## Project Context
- **GCP Project ID**: raffy-cicd-lab-bf9b4f
- **Region**: northamerica-northeast1
- **Artifact Registry**: northamerica-northeast1-docker.pkg.dev/raffy-cicd-lab-bf9b4f/hello-world-app
- **Image name**: hello-world-app
- **Cloud Deploy Pipeline**: hello-world-pipeline
- **Environments**: dev, staging, prod (each is a separate Cloud Run service)

## Conventions
- TypeScript strict mode always on
- Port is always read from process.env.PORT with fallback to 3000
- GET /healthz must return 200 { status: "ok" } — Cloud Run startup probe depends on it
- Image tagged with full git SHA
- Cloud Deploy (not GitHub Actions) handles the actual deployment to Cloud Run

## CLI Tools
node, npm, docker, gcloud, git
