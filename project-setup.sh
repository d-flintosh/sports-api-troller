PROJECT_ID="sports-data-service"

gcloud beta builds triggers create cloud-source-repositories \
    --repo=d-flintosh/sports-api-troller.git \
    --branch-pattern="^master$" \
    --build-config=./cloud-build.yaml