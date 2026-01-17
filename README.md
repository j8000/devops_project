# DevOps Project

## Description
Complete environment for a Flask + Nginx + PostgreSQL web application.
Fully Dockerized with CI/CD pipelines and Azure IaC.

## Project Structure
```
app/
├── src/        # Flask application code
├── tests/      # Pytest tests
├── seed/       # Database seeder script
├── migrations/ # Database migrations
└── requirements.txt
docker/         # Docker configurations (Nginx)
infra/          # Azure Bicep IaC
.github/        # CI/CD Workflows
```

## Running Locally

1. **Start the environment:**
   ```bash
   docker compose up --build
   ```
2. **Access the application:**
   - Web App: `http://localhost`
   - Health Check: `http://localhost/health`

3. **Verify Data:**
   - Seeder output: Check `./seed_output/` folder.
   - Nginx Logs: Check `./nginx_logs/` folder.

## CI/CD
- **CI**: Runs on every push. Builds images, runs tests, scans code.
- **CD**: Runs on tags/manual. Pulls images and restarts app.

## Infrastructure
Deploy Azure resources (Resource Group + ACR):
```bash
az deployment sub create --location eastus --template-file infra/main.bicep --parameters infra/parameters.json
```
