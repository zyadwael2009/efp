"""
Remove catalog, orders, storefront users, and contact messages. Keeps admins and categories.
Run:  python backend/scripts/clear_store_data.py   (from repo root)
   or python scripts/clear_store_data.py          (from backend/)
"""
from __future__ import annotations

import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_ROOT))

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models import ContactMessage, Order, OrderItem, Product, Review, User  # noqa: E402


def main() -> None:
    app = create_app()
    with app.app_context():
        OrderItem.query.delete()
        Order.query.delete()
        Review.query.delete()
        Product.query.delete()
        ContactMessage.query.delete()
        User.query.delete()
        db.session.commit()
        print("Cleared: order items, orders, reviews, products, contact messages, users.")
        print("Kept: admins, categories.")


if __name__ == "__main__":
    main()
