import os
from dotenv import load_dotenv
# Import your Flask app instance and db object from your main app file
from app import app, db 

# This part is just for local testing if you run this script locally
load_dotenv() 

with app.app_context():
    # This will create the tables defined by your 'Users' model
    db.create_all()
    print("Database tables created successfully!")