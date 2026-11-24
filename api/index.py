import sys
import os
import urllib.parse
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from web.flask_app import app

class VercelPathMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        qs = environ.get('QUERY_STRING', '')
        params = urllib.parse.parse_qs(qs)
        if 'path' in params and params['path']:
            path_val = params['path'][0]
            environ['PATH_INFO'] = '/' + path_val.lstrip('/')
        else:
            path = environ.get('PATH_INFO', '')
            if path.startswith('/api/index'):
                environ['PATH_INFO'] = path[len('/api/index'):] or '/'
        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathMiddleware(app.wsgi_app)

if __name__ == "__main__":
    app.run()
