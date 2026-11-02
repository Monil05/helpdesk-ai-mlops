# Project: HelpDesk AI – MLOps Ticketing System

Act as a senior Python developer and MLOps engineer. Help me build a complete but relatively simple project for my **MLOps college course**.

I am a B.Tech Data Science student. The purpose of this project is to demonstrate an end-to-end MLOps workflow, not to build a complicated machine learning model.

I need a working ticketing application, deployed on Azure, along with the infrastructure and monitoring technology stack described below.

## 1. Project description

Build **HelpDesk AI**, an IT helpdesk ticketing system that uses machine learning to automatically classify incoming support tickets.

A user should be able to submit a ticket describing an IT issue, for example:

"My laptop is not connecting to the office Wi-Fi."

The application should:
- Accept a ticket title and description.
- Predict the ticket category using a trained ML model.
- Show the predicted category and prediction confidence.
- Let the user select the ticket priority: Low, Medium or High.
- Generate a unique ticket ID.
- Save the ticket.
- Show all submitted tickets in a dashboard.
- Allow filtering tickets by category, priority and status.
- Allow changing ticket status: New, In Progress or Resolved.
- Show summary statistics such as total tickets, open tickets and resolved tickets.

This is a demonstration application. Do not build unnecessary features such as user authentication, payment systems, email integrations or complex role management.

Use SQLite for ticket storage. Make the database implementation simple and understandable.

## 2. Dataset and machine learning

The dataset is already present in the project's `data/` folder.

First inspect the contents of the folder and identify the correct CSV file and its columns.

The expected dataset structure is:
- `Document`: ticket description.
- `Topic_group`: ticket category.

Do not blindly assume these column names. Verify the actual file and schema before writing the training code.

Use:
- Python
- Pandas
- Scikit-learn
- TF-IDF Vectorizer
- Logistic Regression

Training requirements:
1. Clean the dataset and handle missing values.
2. Remove invalid rows and handle duplicates appropriately.
3. Perform a stratified train/test split.
4. Use a reproducible random seed.
5. Train a TF-IDF + Logistic Regression pipeline.
6. Evaluate using accuracy, precision, recall, F1-score and a confusion matrix.
7. Save the complete trained pipeline using Joblib.
8. Save model evaluation information in a JSON file.

The application must load the saved pipeline and use it for predictions. It must not retrain the model every time the Streamlit application starts.

Priority should be selected by the user. Do not pretend that the model predicts priority because the dataset does not necessarily contain priority labels.

Do not fabricate dataset contents or model evaluation results. Do not generate synthetic data unless the existing dataset is unusable; in that case, explain the problem and ask me first.

Do not publish the original dataset to GitHub or include it in the Docker image by default. Inspect its size, licence and contents first. Keep raw data out of the public image and use the saved model artifact for inference.

## 3. Application and frontend

Use Streamlit.

Keep the interface clean, modern and understandable.

Suggested pages:

**Submit Ticket**
- Ticket title.
- Ticket description.
- Priority selection.
- Submit button.
- Display ticket ID, predicted category and confidence after submission.

**Ticket Dashboard**
- Total tickets.
- New tickets.
- In-progress tickets.
- Resolved tickets.
- Ticket table with ID, title, category, priority, status and date.
- Filters and search.
- Ability to update ticket status.

**Model Information**
- Model name and algorithm.
- Dataset details.
- Evaluation metrics.
- Class distribution.

Use a simple SQLite database to persist tickets. Keep application logic separate from the Streamlit UI.

## 4. Required MLOps technology stack

All the following are mandatory for my course project.

### A. GitHub – Version Control
- Organise the project as a Git repository.
- Maintain a clean `.gitignore`.
- Keep source code, configurations and documentation version-controlled.
- Do not commit credentials, Terraform state, raw datasets or private keys.
- Create a proper README.

Do not create a remote GitHub repository or push code until I approve it.

### B. GitHub Actions – CI/CD
Create GitHub Actions workflows.

CI should:
- Run whenever code is pushed or a pull request is opened.
- Install Python dependencies.
- Run automated tests using Pytest.
- Validate that the model can load and make predictions.
- Build the Docker image.

CD should:
- Build and tag the Docker image.
- Publish the image to GitHub Container Registry (GHCR).
- Provide a deployment workflow for Azure Kubernetes Service.
- Prefer secure GitHub OIDC authentication over long-lived credentials.
- Do not store credentials or kubeconfig files in the repository.

Use GitHub Actions' `GITHUB_TOKEN` for publishing images where possible.

If Azure deployment automation requires additional configuration, implement the workflow and clearly document the required setup. Do not pretend a deployment workflow is functional until tested.

### C. Docker
Create:
- A clean Dockerfile.
- A `.dockerignore`.
- A local `docker-compose.yml` for testing the application and monitoring services.

The Docker image should contain the application, required dependencies and trained model artifact.

Do not include the original training dataset in the image.

The application must run inside Docker and expose Streamlit on port 8501.

### D. Kubernetes
Use Azure Kubernetes Service (AKS) for the actual Azure deployment.

Create understandable Kubernetes YAML manifests for:
- Namespace.
- Application Deployment.
- Application Service.
- Prometheus Deployment and Service.
- Grafana Deployment and Service.
- Required ConfigMaps and Secrets.

Requirements:
- Run one application replica initially.
- Use sensible CPU and memory requests/limits.
- Include readiness and liveness probes.
- Expose the Streamlit application through an Azure LoadBalancer Service.
- Keep Prometheus and Grafana internal to the cluster, using port-forwarding for dashboard access.
- Do not expose the Prometheus metrics endpoint publicly.

Keep the SQLite implementation suitable for a short demonstration. Clearly document whether ticket records persist across pod replacement.

### E. Terraform – Infrastructure as Code
Use Terraform with the AzureRM provider.

Terraform must define the infrastructure needed for the project:
- Azure Resource Group.
- Azure Kubernetes Service cluster.

Cost requirements:
- Use the AKS Free control-plane tier.
- Use one small, suitable worker node.
- Disable autoscaling for this demonstration.
- Avoid unnecessary Azure services.
- Do not provision Azure Container Registry; use GHCR instead.
- Do not provision Azure Managed Grafana or Azure Monitor managed Prometheus; deploy the open-source versions inside Kubernetes.
- Do not provision expensive services such as Azure Firewall, Bastion, NAT Gateway or Application Gateway.

Use configurable Terraform variables for region, resource names and VM size.

Check region availability and subscription quota before recommending a VM SKU. Do not assume that a particular VM SKU is available.

Keep Terraform state and `.tfvars` files out of Git.

### F. Prometheus and Grafana – Monitoring
Instrument the Python application using `prometheus-client`.

Expose an application metrics endpoint on port 8000.

Include metrics such as:
- Total tickets submitted.
- Total predictions.
- Predictions by category.
- Prediction latency.
- Prediction errors.
- Tickets by status.

Avoid using ticket descriptions, ticket IDs or other high-cardinality values as Prometheus labels.

Configure Prometheus to scrape the application's internal metrics endpoint.

Configure Grafana with:
- Prometheus as its data source.
- A preconfigured dashboard.
- Panels for total predictions, category distribution, errors, latency and ticket counts.

The dashboard must work with actual application activity, not fabricated metric data.

## 5. Azure deployment and cost constraints

I have an **Azure for Students subscription with $100 in credits for 12 months**.

The main purpose is to demonstrate a working deployment for my college course. I only need the application and technology stack running long enough for a presentation.

I do not want to consume all my Azure credits.

Minimise resource usage and running time. Do not keep the cluster running unnecessarily.

Use GHCR to avoid Azure Container Registry charges.

Use self-hosted Prometheus and Grafana inside AKS instead of paid managed monitoring services.

Before proposing Azure infrastructure:
1. Check that Azure CLI is installed.
2. Check that I am logged in.
3. Check that the active subscription is my Azure for Students subscription.
4. Check available region and VM quota.
5. Estimate the infrastructure cost for approximately 4 hours and 24 hours.
6. Explain which resources are billable and why.
7. Recommend the cheapest practical configuration that can run the application and monitoring stack.

Do not blindly assume the $100 credit makes every Azure service free.

### CRITICAL AZURE SAFETY RULE

**Never create, modify or delete actual Azure resources without asking me first and receiving explicit approval.**

You may:
- Install local development dependencies.
- Write Terraform files.
- Write Kubernetes manifests.
- Run Terraform formatting and validation.
- Run local Docker builds and tests.
- Perform read-only Azure account, quota and availability checks.
- Generate a Terraform plan for review.

You must STOP before:
- `terraform apply`
- `az aks create`
- Creating an Azure Resource Group.
- Creating a VM, storage account, public IP or other billable resource.
- Any other command that creates or modifies Azure infrastructure.

Before asking for approval, show me:
- The exact resources to be created.
- VM size and node count.
- Azure region.
- Estimated hourly and 4-hour costs.
- Any additional networking, storage or public IP charges.
- The total estimated cost for the demonstration.

Do not upgrade my Azure subscription to Pay-As-You-Go. Do not enable paid services without my approval.

Never automatically destroy resources either. Ask me before running `terraform destroy` or deleting an Azure resource.

## 6. Local development environment and dependency installation

I am using Windows, VS Code and the Codex extension.

First inspect which tools are installed:

- Python 3.10+ (prefer Python 3.12 if compatible).
- Git.
- Docker Desktop with Docker Compose.
- Azure CLI.
- Terraform CLI.
- kubectl.

Install missing project Python dependencies inside a virtual environment. Do not install Python packages globally.

If a required system tool is missing, use its official Windows installation method. You may use WinGet where appropriate, but request approval for system-wide installation or administrator access.

Azure CLI installation, if missing:
`winget install --exact --id Microsoft.AzureCLI`

Verify installations using their version commands.

Do not ask me to manually create files that you can create in the project workspace.

For Azure authentication, I will complete the browser login myself. Do not change subscriptions without checking with me first.

## 7. Recommended project folder structure

Keep the structure clean and understandable. Avoid creating dozens of unnecessary files.

Use a structure similar to:

```text
HelpDesk-AI/
│
├── app/
│   ├── streamlit_app.py
│   ├── database.py
│   ├── classifier.py
│   └── metrics.py
│
├── ml/
│   ├── train.py
│   └── evaluate.py
│
├── data/
│   └── existing_dataset.csv
│
├── models/
│   ├── ticket_classifier.joblib
│   └── model_metadata.json
│
├── tests/
│   ├── test_classifier.py
│   ├── test_database.py
│   └── test_app_logic.py
│
├── infra/
│   └── terraform/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── versions.tf
│
├── k8s/
│   ├── namespace.yaml
│   ├── app.yaml
│   ├── prometheus.yaml
│   └── grafana.yaml
│
├── monitoring/
│   ├── prometheus.yml
│   └── grafana/
│       ├── datasources/
│       └── dashboards/
│
├── .github/
│   └── workflows/
│       ├── ci-cd.yml
│       └── deploy-aks.yml
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
├── .dockerignore
├── .gitignore
└── README.md
```

You can adjust the structure if there is a good technical reason, but keep it easy for a student to understand and explain.

## 8. How I want you to execute the project

Work in stages. Do not attempt to create the entire project in one unverified step.

**Stage 1 – Inspect and prepare**
- Inspect my current workspace and dataset.
- Check installed tools.
- Install missing local dependencies with approval where needed.
- Explain the dataset columns and categories.

**Stage 2 – ML and application**
- Train and evaluate the classifier.
- Build the Streamlit ticketing system.
- Implement SQLite storage.
- Implement Prometheus metrics.
- Run automated tests.
- Verify the application locally.

**Stage 3 – Docker**
- Create the Dockerfile and Docker Compose configuration.
- Build and run the application locally.
- Verify the app and metrics endpoint work.

**Stage 4 – GitHub and CI/CD**
- Prepare the Git repository.
- Create GitHub Actions workflows.
- Build and publish the Docker image to GHCR after I approve the GitHub push/package setup.
- Prepare the Azure deployment workflow.

**Stage 5 – Kubernetes and Terraform**
- Create and validate Kubernetes manifests.
- Create and validate Terraform configuration.
- Check Azure quota, region availability and estimated cost.
- Generate the deployment plan.
- STOP and ask for approval before creating any Azure resources.

**Stage 6 – Actual Azure deployment**
Only after I approve:
- Provision AKS through Terraform.
- Retrieve cluster credentials.
- Deploy the application.
- Deploy Prometheus and Grafana.
- Verify the Streamlit public endpoint.
- Verify that metrics reach Prometheus and Grafana.
- Test the GitHub Actions deployment workflow if configured.

**Stage 7 – Presentation preparation**
Prepare a concise README explaining:
- What the project does.
- Dataset and ML model.
- How training works.
- How Docker is used.
- How GitHub Actions works.
- How Kubernetes manages the application.
- What Terraform provisions.
- What Prometheus and Grafana monitor.
- Azure deployment architecture.
- Commands to start, inspect and stop the project.
- How to clean up Azure resources after the demonstration.

Also give me a simple explanation of the complete architecture that I can use when presenting this project to my professor.

## 9. Quality expectations

- Write clean, readable and modular code.
- Include useful comments, not comments on every line.
- Avoid unnecessary abstraction and overengineering.
- Use environment variables for configuration and secrets.
- Never hardcode credentials.
- Include error handling and meaningful error messages.
- Test the actual implementation rather than only creating files.
- Do not claim a feature works until it has been tested.
- Explain errors and fix them rather than silently ignoring them.
- Do not replace an existing dataset or overwrite unrelated workspace files.
- Do not invent successful deployment output.

Maybe push to github as you are making the project as well to make it have at least 2-3 commits in commit history.
DONT PUSH ANY SENSITIVE INFO/ENV/API keys to github, azure or anywhere else.