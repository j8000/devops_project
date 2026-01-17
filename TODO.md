# DevOps Project TODO List

Based on the requirements from `projekt_devops.pdf`.

## 1. Project Initialization & Structure
- [ ] **Create Directory Structure**:
    - `app/src/` (Application code)
    - `app/tests/` (Pytest tests)
    - `app/seed/` (Seeder script `run_seed.py`)
    - `app/migrations/` (Database migrations)
    - `docker/` (Nginx conf, scripts)
    - `infra/` (Azure IaC)
    - `.github/workflows/` (CI/CD)
    - Root files: `Dockerfile`, `docker-compose.yml`, `README.md`, `app/requirements.txt`
- [ ] Initialize git repository.

## 2. Flask Application (`app/src`)
- [ ] **Dependencies**: `app/requirements.txt` (Flask, psycopg2, sqlalchemy, pytest, etc.).
- [ ] **Application Logic**:
    - [ ] Endpoint `/health`.
    - [ ] 2-3 Business endpoints (e.g., `/users`, `/tasks`).
    - [ ] Database Connection (PostgreSQL).
    - [ ] Models: `User`, `Task`, `Product` (min 3 models).
- [ ] **Tests (`app/tests`)**:
    - [ ] Unit test.
    - [ ] Logic test.
    - [ ] HTTP endpoint test.
    - [ ] *Requirement*: Run in Docker `test` stage.

## 3. Database, Migrations & Seeding
- [ ] **Migrations**:
    - [ ] Setup migration tool (e.g., Flask-Migrate/Alembic) in `app/migrations/`.
    - [ ] (Optional) Create `migration_runner` service in Docker Compose.
- [ ] **Seeder (`app/seed/run_seed.py`)**:
    - [ ] Script (Python) to populate DB (min 5 records).
    - [ ] Generate output files: `seed.log`, `users.csv`, `data.json`.
    - [ ] Write to volume: `/seed_output`.
    - [ ] *Requirement*: Execute *after* migrations.

## 4. Docker Configuration
- [ ] **Dockerfile** (Multi-stage):
    - [ ] **Stage 1: Builder**: Install deps from `app/requirements.txt`, copy `app/`.
    - [ ] **Stage 2: Test**: Inherit builder, run `pytest`. Fail build on error.
    - [ ] **Stage 3: Final**: Python-slim, copy artifacts, runtime ready.
- [ ] **Nginx Config (`docker/nginx.conf`)**:
    - [ ] Reverse proxy to Flask app.
    - [ ] Log to `/var/log/nginx` (mounted volume).
- [ ] **Docker Compose (`docker-compose.yml`)**:
    - [ ] **Networks**: `front_net` (Public), `back_net` (Internal).
    - [ ] **Volumes**: `db_data`, `nginx_logs`, `seed_output`.
    - [ ] **Service `app`**: Final image, `front_net` + `back_net`, depends on `db`.
    - [ ] **Service `nginx`**: `front_net`, ports `80:80`, volume `nginx_logs`.
    - [ ] **Service `db`**: PostgreSQL, `back_net`, volume `db_data`.
    - [ ] **Service `seed_runner`**:
        - [ ] Connects to DB (`back_net`).
        - [ ] Runs `app/seed/run_seed.py`.
        - [ ] Mounts `seed_output`.
        - [ ] `restart: "no"`.
        - [ ] Depends on `db` (and `migration_runner` if exists).

## 5. Infrastructure as Code (Azure)
- [ ] **Files (`infra/`)**:
    - [ ] `main.bicep` (or ARM): Resource Group, ACR.
    - [ ] `parameters.json`.
    - [ ] (Optional) Storage Account.
- [ ] **Constraint**: Azure used ONLY for IaC + Registry. App runs locally/Docker.

## 6. GitHub Actions (CI/CD)
- [ ] **CI Pipeline (`.github/workflows/ci.yml`)**:
    - [ ] Trigger: `push`, `pull_request`.
    - [ ] Steps: Checkout -> Build (builder) -> Test (pytest) -> Build (final) -> Push to ACR/GHCR -> CodeQL Scan.
- [ ] **CD Pipeline (`.github/workflows/cd.yml`)**:
    - [ ] Trigger: `workflow_dispatch` or tags.
    - [ ] Steps: Pull images -> `docker compose up -d` -> Restart app.

## 7. Verification
- [ ] Check `nginx_logs` volume content.
- [ ] Check `seed_output` volume content (files generated).
- [ ] Check DB persistence (`db_data`).
- [ ] Verify `front_net` isolates DB from public.
