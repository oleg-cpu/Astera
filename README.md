# Astera Task Manager

A production-ready Django Task Management application deployed on AWS infrastructure using modern DevOps practices, Infrastructure as Code (IaC), CI/CD, and Automated Configuration Management.

---

## 🛠️ Tech Stack & Architecture

* **Backend:** Python 3.13 / Django
* **Database:** AWS RDS (PostgreSQL)
* **Infrastructure (IaC):** Terraform (VPC, EC2, RDS, Security Groups)
* **Configuration Management:** Ansible
* **Containerization:** Docker & Docker Compose
* **Reverse Proxy / Web Server:** Nginx
* **CI/CD Pipeline:** GitHub Actions & GitHub Container Registry (GHCR)
* **Cloud Provider:** AWS (Amazon Web Services)

---

## 🚀 CI/CD & Automated Quality Gate

The project uses a GitHub Actions pipeline (`deploy.yml`) to enforce code quality before any deployment:
1.  **Testing-and-Linting Job:** Runs Django unit tests using an isolated, fast in-memory SQLite database (`test_settings.py`) and checks code formatting via `pre-commit` (Ruff, Mypy).
2.  **Build-and-Push Job:** If all tests and linters pass successfully, it builds the Docker image and pushes it to GHCR. Merges to the `main` branch automatically tag the image as `latest` for production use.

---

## ☁️ Cloud Deployment Guide (AWS)

Follow this comprehensive guide to provision the infrastructure and configure/deploy the application to the AWS cloud.

### 📋 Prerequisites
* An AWS Account with configured CLI credentials.
* Terraform installed locally.
* Ansible installed (via Linux/WSL/macOS).
* An SSH key pair registered in your AWS dashboard.

### Step 1: Provision Infrastructure with Terraform
1. Navigate to your `terraform/` directory.
2. Initialize and apply the configuration:
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```
### Step 2: Configure Ansible Deployment Variables
1. Navigate to your `ansible/` directory.
2. Create your deployment configuration secrets file named `secret_vars.yml` and paste the following block, replacing the placeholders with your actual AWS infrastructure and secure credentials:

```bash
django_secret_key: "your-super-secret-key-here"
django_allowed_hosts: "YOUR_EC2_PUBLIC_IP_OR_DOMAIN"
rds_db_name: "dbname"
rds_db_user: "userdb"
rds_db_password: "secure-password"
rds_db_host: "YOUR_RDS_ENDPOINT_FROM_TERRAFORM_OUTPUT"
rds_db_port: "5432"
```

### Step 3: Configure Ansible Host Inventory
1. In the same `ansible/` directory, create your server inventory file named hosts.ini.
2. Paste the configuration block below, ensuring you provide your real EC2 instance IP and the local path to your AWS private SSH key (.pem file):

```bash
[webservers]
ec2-instance ansible_host=YOUR_EC2_PUBLIC_IP ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/YOUR_KEY.pem

[webservers:vars]
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
```
### Step 4: Run the Deployment Playbook
Execute Ansible to automatically install Docker, set up Nginx as a reverse proxy, inject your secrets, and spin up your application containers via `docker-compose`

```bash
ansible-playbook -i hosts.ini playbook.yml
```

### Local Development & Testing

To run Django unit tests locally on your machine without needing a connection to the production PostgreSQL container or AWS RDS instance:
```bash
python manage.py test tasks --settings=config.test_settings
```
### Code Linting
This project uses pre-commit hooks. To run formatting and code-quality checks manually across all files
```bash
pre-commit run --all-files
```
