import os
import sys
import time
import csv
import json
import logging
from sqlalchemy import text

# Add the application root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.src.db import init_db, db_session
from app.src.models import User, Task, Product

# Configuration
# Docker volume path should be mapped here. Default to local for testing if needed.
OUTPUT_DIR = os.environ.get("SEED_OUTPUT_DIR", "/seed_output")
LOG_FILE = os.path.join(OUTPUT_DIR, "seed.log")

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    except OSError:
        # Fallback if permission denied (e.g. locally without sudo), though in Docker it should work
        print(f"Warning: Could not create {OUTPUT_DIR}. Logging to stdout.")
        LOG_FILE = None

# Setup logging
handlers = [logging.StreamHandler()]
if LOG_FILE:
    handlers.append(logging.FileHandler(LOG_FILE))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=handlers
)

def run_seed():
    logging.info("Starting database seeding...")
    
    try:
        # In a real scenario, we wait for the DB to be ready.
        # Here we assume it's ready or handled by docker depends_on/restart policies.
        
        logging.info("Initializing/Checking database tables...")
        # Ensure tables exist (if migrations didn't run or this is used as init)
        init_db()
        
        # Check if data exists
        if User.query.first():
            logging.info("Data already exists. Skipping insertion.")
        else:
            logging.info("Inserting sample data...")
            
            # Create Users
            users = [
                User(name="Alice", email="alice@example.com"),
                User(name="Bob", email="bob@example.com"),
                User(name="Charlie", email="charlie@example.com"),
                User(name="Dave", email="dave@example.com"),
                User(name="Eve", email="eve@example.com")
            ]
            db_session.add_all(users)
            
            # Create Tasks
            tasks = [
                Task(title="Fix bug #1", status="pending"),
                Task(title="Write documentation", status="completed"),
                Task(title="Deploy to prod", status="pending")
            ]
            db_session.add_all(tasks)
            
            # Create Products
            products = [
                Product(name="Laptop", price=150000),
                Product(name="Mouse", price=2500),
                Product(name="Keyboard", price=5000)
            ]
            db_session.add_all(products)
            
            db_session.commit()
            logging.info(f"Inserted {len(users)} users, {len(tasks)} tasks, {len(products)} products.")

        # Export data to files
        export_users()
        export_summary()
        
        logging.info("Seeding completed successfully.")
        
    except Exception as e:
        logging.error(f"Seeding failed: {e}")
        db_session.rollback()
        sys.exit(1)
    finally:
        db_session.remove()

def export_users():
    users = User.query.all()
    csv_path = os.path.join(OUTPUT_DIR, "users.csv")
    logging.info(f"Exporting users to {csv_path}...")
    
    try:
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Name', 'Email'])
            for u in users:
                writer.writerow([u.id, u.name, u.email])
    except IOError as e:
        logging.error(f"Failed to write users.csv: {e}")

def export_summary():
    try:
        data = {
            "user_count": User.query.count(),
            "task_count": Task.query.count(),
            "product_count": Product.query.count(),
            "timestamp": time.time()
        }
        json_path = os.path.join(OUTPUT_DIR, "data.json")
        logging.info(f"Exporting summary to {json_path}...")
        
        with open(json_path, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=4)
    except Exception as e:
        logging.error(f"Failed to write summary: {e}")

if __name__ == "__main__":
    run_seed()
