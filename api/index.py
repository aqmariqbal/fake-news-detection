import sys
import os
from pathlib import Path

# Add project root to sys.path so modules in src/ and web/ are discoverable
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Import Flask app instance from web/flask_app.py
from web.flask_app import app

# Vercel entrypoint expects the WSGI application object 'app'
if __name__ == "__main__":
    app.run()
