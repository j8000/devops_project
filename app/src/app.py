from flask import Flask, jsonify
from app.src.db import db_session, init_db
from app.src.models import User, Task, Product

app = Flask(__name__)

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
    try:
        init_db()
    except Exception as e:
        print(f"DB init failed (expected during build/test without DB): {e}")
    
    app.run(host='0.0.0.0', port=5000)
