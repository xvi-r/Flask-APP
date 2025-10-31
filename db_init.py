# db_init.py

import sys
from app import app, db # Import app and db instance
from models import * # Import all models (Users, Streamer, TF2_Networks, etc.)
from sqlalchemy.exc import OperationalError

def init_db(action="create"):
    """Initializes or resets the database schema."""
    
    with app.app_context():
        if action == "drop":
            print("🛑 WARNING: Dropping ALL tables...")
            db.drop_all()
            print("Tables dropped successfully.")
            
        elif action == "create":
            print("Creating missing tables...")
            # This creates tables only if they don't already exist.
            db.create_all()
            print("Database initialization complete.")

        else:
            print("Error: Invalid action specified. Use 'create' or 'drop'.")
            sys.exit(1)


if __name__ == "__main__":
    # --- Execution Logic ---
    # This allows you to run it like: python db_init.py create
    # Or: python db_init.py drop

    action = "create" # Default action if no argument is provided
    
    if len(sys.argv) > 1:
        action = sys.argv[1].lower()

    # The creation command is now run using the function
    init_db(action=action)