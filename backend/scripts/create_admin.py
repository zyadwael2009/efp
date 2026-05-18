"""
Create or update an admin account (bootstrap is disabled by default in the API).
Run:  python backend/scripts/create_admin.py --email you@example.com --password "YourPassword" --name "Your Name"
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_ROOT))

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models import Admin  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--name", default="Administrator")
    args = parser.parse_args()

    email = args.email.strip().lower()
    password = args.password
    name = args.name.strip() or "Administrator"

    if len(password) < 8:
        print("Error: password must be at least 8 characters.")
        sys.exit(1)

    app = create_app()
    with app.app_context():
        admin = Admin.query.filter_by(email=email).first()
        if admin:
            admin.name = name
            admin.set_password(password)
            action = "Updated"
        else:
            admin = Admin(name=name, email=email)
            admin.set_password(password)
            db.session.add(admin)
            action = "Created"

        db.session.commit()
        print(f"{action} admin: {email}")


if __name__ == "__main__":
    main()
