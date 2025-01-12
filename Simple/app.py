# app.py
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
with open('/run/secrets/db-password', 'r') as password_file:
    db_password = password_file.read().strip()
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://postgres:{db_password}@db:5432/example"
)

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Define a simple model
class Example(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/')
def hello():
    return "Hello, Docker!"

@app.route('/examples')
def show_examples():
    # Create tables if they don't exist
    db.create_all()
    
    # Add a default entry if none exists
    if not Example.query.first():
        example_entry = Example(name="Test Entry")
        db.session.add(example_entry)
        db.session.commit()
    
    # Fetch and return all rows
    examples = Example.query.all()
    return jsonify([{'id': ex.id, 'name': ex.name} for ex in examples])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)