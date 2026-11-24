import sys
import os
from pathlib import Path

# Add project root to sys.path so modules in src/ and web/ are discoverable
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Import Flask app instance from web/flask_app.py
from web.flask_app import app

# Strip '/api/index' or '/api' prefix injected by Vercel rewrites
class VercelPrefixMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        if path.startswith('/api/index'):
            environ['PATH_INFO'] = path[len('/api/index'):] or '/'
        elif path.startswith('/api'):
            environ['PATH_INFO'] = path[len('/api'):] or '/'
        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPrefixMiddleware(app.wsgi_app)

if __name__ == "__main__":
    app.run()
