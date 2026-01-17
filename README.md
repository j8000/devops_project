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

## Screenshots
<img width="1317" height="164" alt="image" src="https://github.com/user-attachments/assets/04601985-9251-4545-b667-d6d206b4956e" />

<img width="676" height="164" alt="image" src="https://github.com/user-attachments/assets/3cbfb911-e516-4652-928a-90cafeae1194" />

<img width="1623" height="70" alt="image" src="https://github.com/user-attachments/assets/4685fbd4-b311-4c4e-834b-5ab5fbb68948" />

