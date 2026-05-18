"""
WSGI entry point for PythonAnywhere (and any WSGI-compatible server).

PythonAnywhere setup:
1. In the Web tab, set "Source code" to /home/<username>/efp/backend
2. Set "Working directory" to /home/<username>/efp/backend
3. Set "WSGI configuration file" path to this file
4. In the WSGI file editor on PythonAnywhere, replace its contents with
   the import below (adjusting the path to match your username):

       import sys
       sys.path.insert(0, '/home/<username>/efp/backend')
       from wsgi import application

   Or simply point PythonAnywhere directly at this file.

5. Create a .env file in /home/<username>/efp/backend/ with your settings
   (see .env.example), then reload the web app.
6. Open a PythonAnywhere Bash console and run:
       cd ~/efp/backend
       python scripts/create_admin.py --email your@email.com --password "YourPassword"
"""
import sys
import os
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# Load .env if present (python-dotenv is in requirements.txt)
try:
    from dotenv import load_dotenv
    load_dotenv(BACKEND_DIR / ".env")
except Exception:
    pass

from app import create_app  # noqa: E402

application = create_app()
