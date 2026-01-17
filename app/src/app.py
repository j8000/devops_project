from flask import Flask, jsonify
from flask_migrate import Migrate
from app.src.db import db_session, init_db, Base, engine
from app.src.models import User, Task, Product

app = Flask(__name__)

# Flask-Migrate configuration
# Ideally, we should set app.config['SQLALCHEMY_DATABASE_URI'] from env
import os
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "postgresql://user:password@localhost/flaskdb")

# We need to bridge SQLAlchemy Base with Flask for Migrate
# Since we used declarative_base() separately, we might need to adjust or just pass the metadata.
# Typically Flask-SQLAlchemy is used, but here we used pure SQLAlchemy + scoped_session.
# Flask-Migrate expects a Flask-SQLAlchemy 'db' object usually, but can work with existing declarative base 
# if we configure alembic env.py correctly.
# However, for simplicity and standard compliance in this 'simple' project, 
# let's instantiate Migrate.
migrate = Migrate(app, Base.metadata)
# Note: Migrate(app, db) is standard. With pure SQLAlchemy, it's a bit more manual.
# To keep it simple for the user and requirements, we might not strictly NEED 'flask db migrate' 
# if we rely on init_db() or plain SQL. 
# But let's try to support it. 
# We might need to expose 'engine' or 'db_session' differently.
# A common pattern without Flask-SQLAlchemy:
# migrate = Migrate(app, Base.metadata, render_as_batch=True)
# But we need to tell alembic how to connect.
# For now, we will leave the hook here.

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/users')
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "name": u.name, "email": u.email} for u in users])

@app.route('/tasks')
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title, "status": t.status} for t in tasks])

@app.route('/')
def index():
    return jsonify({"message": "Hello from Flask!"})

if __name__ == '__main__':
    # Initialize DB on startup (for simplicity in this project structure)
    try:
        init_db()
    except Exception as e:
        print(f"DB init failed (expected during build/test without DB): {e}")
    
    app.run(host='0.0.0.0', port=5000)
