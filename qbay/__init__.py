import os
import sys
from qbay.database import db, app

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

templates = os.path.join(SCRIPT_DIR, "templates")

# Drop existing database and create new instance
with app.app_context():
    db.drop_all()
    db.create_all()
