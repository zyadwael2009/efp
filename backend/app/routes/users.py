from flask import Blueprint, jsonify, request

from ..extensions import db
from ..models import ContactMessage, User


users_bp = Blueprint("users", __name__)


@users_bp.get("/users")
def list_users():
    limit = max(1, min(request.args.get("limit", 25, type=int), 100))
    users = User.query.order_by(User.created_at.desc()).limit(limit).all()
    return jsonify({"items": [user.to_dict() for user in users]})


@users_bp.get("/users/<int:user_id>")
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())


@users_bp.post("/users")
def create_or_update_user():
    payload = request.get_json(silent=True) or {}

    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip().lower()

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    marketing_opt_in = bool(payload.get("marketing_opt_in", True))

    user = User.query.filter_by(email=email).first()
    status = 201
    message = "User created"

    if user:
        user.name = name
        user.marketing_opt_in = marketing_opt_in
        status = 200
        message = "User updated"
    else:
        user = User(name=name, email=email, marketing_opt_in=marketing_opt_in)
        db.session.add(user)

    db.session.commit()
    return jsonify({"message": message, "user": user.to_dict()}), status


@users_bp.post("/users/contact")
def create_contact_message():
    payload = request.get_json(silent=True) or {}

    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip().lower()
    message = (payload.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify({"error": "Name, email, and message are required"}), 400

    contact_message = ContactMessage(name=name, email=email, message=message)
    db.session.add(contact_message)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Contact request received",
                "contact": contact_message.to_dict(),
            }
        ),
        201,
    )
