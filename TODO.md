# TODO List

## 1. Enhance Helm Charts
- Populate `helm-charts/Chart.yaml` and `helm-charts/values.yaml` with meaningful content.
- Add templates for Kubernetes resources (e.g., Deployment, Service).

## 2. Improve Documentation
- Expand the `README` to include:
  - Project overview.
  - Steps to build and run the application locally and in Docker.
  - CI/CD pipeline usage.
  - Helm chart deployment instructions.

## 3. Add Tests
- Include unit tests for Python code.
- Add integration tests for the CI/CD pipeline.

## 4. Secure Credentials
- Ensure sensitive credentials (e.g., Docker Hub credentials, GitHub PAT) are securely stored in Jenkins.
- Avoid exposing sensitive information in logs.

## 5. Complete Missing Files
- Implement or remove empty files like `src/quotes_handler/Dockerfile`.

## 6. Refactor Pipeline
- Modularize the `Jenkinsfile` by moving reusable functions (e.g., `PrintStageName`, `captureRawPayload_method_1`) to a shared library.

## 7. Error Handling in Python
- Add exception handling to `src/frontend/frontend.py` to prevent unexpected crashes.

## 8. Pipeline Optimization
- Externalize hardcoded values in the `Jenkinsfile` (e.g., `APP_VERSION_PREFIX`, `DOCKERHUB_USERNAME`) into environment variables or configuration files.

## 9. Testing Helm Charts
- Validate and test the Helm chart templates to ensure they work as expected.