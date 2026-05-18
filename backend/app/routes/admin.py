import re
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from functools import wraps

from flask import Blueprint, current_app, g, jsonify, request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from ..extensions import db
from ..models import Admin, Category, ContactMessage, Order, Product, User

admin_bp = Blueprint("admin", __name__)

ORDER_STATUSES = {
    "pending",
    "confirmed",
    "processing",
    "shipped",
    "delivered",
    "cancelled",
    "refunded",
}


def _utcnow():
    return datetime.now(timezone.utc)


def _token_serializer():
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt="efp-admin-auth")


def _extract_bearer_token():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.lower().startswith("bearer "):
        return None
    return auth_header.split(" ", 1)[1].strip()


def _generate_admin_token(admin):
    return _token_serializer().dumps({"admin_id": admin.id, "email": admin.email})


def _verify_admin_token(token):
    max_age = int(current_app.config.get("ADMIN_TOKEN_MAX_AGE_SECONDS", 86400))
    data = _token_serializer().loads(token, max_age=max_age)
    admin_id = data.get("admin_id")
    if not admin_id:
        return None
    return Admin.query.get(admin_id)


def _unauthorized(message="Unauthorized"):
    return jsonify({"error": message}), 401


def require_admin(handler):
    @wraps(handler)
    def wrapped(*args, **kwargs):
        token = _extract_bearer_token()
        if not token:
            return _unauthorized("Missing bearer token")

        try:
            admin = _verify_admin_token(token)
        except SignatureExpired:
            return _unauthorized("Session expired")
        except BadSignature:
            return _unauthorized("Invalid token")

        if not admin:
            return _unauthorized("Admin not found")

        g.current_admin = admin
        return handler(*args, **kwargs)

    return wrapped


def _slugify(value):
    raw = (value or "").strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", raw).strip("-")
    return slug


def _to_string_list(value):
    if value is None:
        return []

    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]

    if isinstance(value, str):
        return [part.strip() for part in value.split(",") if part.strip()]

    return []


def _to_decimal(value):
    return Decimal(str(value)).quantize(Decimal("0.01"))


def _to_int(value, default=0):
    if value is None or value == "":
        return default
    return int(value)


def _ensure_unique_product_slug(base_slug, current_product_id=None):
    base_slug = base_slug or "product"
    candidate = base_slug
    suffix = 2

    while True:
        query = Product.query.filter_by(slug=candidate)
        if current_product_id is not None:
            query = query.filter(Product.id != current_product_id)

        if query.first() is None:
            return candidate

        candidate = f"{base_slug}-{suffix}"
        suffix += 1


def _resolve_category(payload):
    category_id = payload.get("category_id")
    category_slug = (payload.get("category_slug") or payload.get("category") or "").strip().lower()
    category_name = (payload.get("category_name") or "").strip()
    category_description = (payload.get("category_description") or "").strip() or None

    if category_id not in (None, ""):
        try:
            category = Category.query.get(int(category_id))
        except (TypeError, ValueError):
            return None, "Invalid category_id"

        if not category:
            return None, "Category not found"

        return category, None

    if category_slug:
        category = Category.query.filter_by(slug=category_slug).first()
        if category:
            return category, None

        inferred_name = category_name or category_slug.replace("-", " ").title()
        category = Category(name=inferred_name, slug=category_slug, description=category_description)
        db.session.add(category)
        db.session.flush()
        return category, None

    if category_name:
        slug = _slugify(category_name)
        if not slug:
            return None, "Invalid category_name"

        category = Category.query.filter_by(slug=slug).first()
        if category:
            return category, None

        category = Category(name=category_name, slug=slug, description=category_description)
        db.session.add(category)
        db.session.flush()
        return category, None

    return None, "A category is required"


def _validate_create_product_payload(payload):
    required_fields = [
        "name",
        "short_description",
        "description",
        "scent",
        "size",
        "burn_time",
        "price",
    ]

    missing = [field for field in required_fields if not str(payload.get(field, "")).strip()]
    if missing:
        return None, f"Missing required fields: {', '.join(missing)}"

    name = payload.get("name", "").strip()
    short_description = payload.get("short_description", "").strip()
    description = payload.get("description", "").strip()
    scent = payload.get("scent", "").strip()
    size = payload.get("size", "").strip()
    burn_time = payload.get("burn_time", "").strip()

    slug_raw = (payload.get("slug") or name).strip()
    slug = _slugify(slug_raw)
    if not slug:
        return None, "Product slug could not be generated"

    try:
        price = _to_decimal(payload.get("price"))
        inventory_count = _to_int(payload.get("inventory_count"), default=0)
    except (TypeError, ValueError, InvalidOperation):
        return None, "Invalid price or inventory_count"

    if inventory_count < 0:
        return None, "inventory_count cannot be negative"

    category, category_error = _resolve_category(payload)
    if category_error:
        return None, category_error

    images = _to_string_list(payload.get("images") or payload.get("image") or payload.get("image_url"))
    materials = _to_string_list(payload.get("materials"))

    return (
        {
            "name": name,
            "slug": _ensure_unique_product_slug(slug),
            "short_description": short_description,
            "description": description,
            "scent": scent,
            "size": size,
            "burn_time": burn_time,
            "materials": materials,
            "images": images,
            "price": price,
            "featured": bool(payload.get("featured", False)),
            "inventory_count": inventory_count,
            "category_id": category.id,
        },
        None,
    )


@admin_bp.post("/admin/bootstrap")
def bootstrap_admin_account():
    if not current_app.config.get("ENABLE_ADMIN_BOOTSTRAP"):
        return jsonify({"error": "Admin bootstrap is disabled. Use a server script or enable ENABLE_ADMIN_BOOTSTRAP."}), 403

    if Admin.query.count() > 0:
        return jsonify({"error": "Admin account already exists. Please login."}), 409

    payload = request.get_json(silent=True) or {}
    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required"}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    required_bootstrap_key = (current_app.config.get("ADMIN_BOOTSTRAP_KEY") or "").strip()
    provided_key = (
        payload.get("bootstrap_key")
        or request.headers.get("X-Admin-Bootstrap-Key")
        or ""
    ).strip()

    if required_bootstrap_key and provided_key != required_bootstrap_key:
        return jsonify({"error": "Invalid bootstrap key"}), 403

    try:
        admin = Admin(name=name, email=email)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Could not create admin account"}), 500

    token = _generate_admin_token(admin)
    return (
        jsonify(
            {
                "message": "Admin account created",
                "admin": admin.to_dict(),
                "token": token,
            }
        ),
        201,
    )


@admin_bp.post("/admin/login")
def admin_login():
    payload = request.get_json(silent=True) or {}

    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    admin = Admin.query.filter_by(email=email).first()
    if not admin or not admin.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    admin.last_login_at = _utcnow()
    db.session.commit()

    token = _generate_admin_token(admin)
    return jsonify({"message": "Login successful", "admin": admin.to_dict(), "token": token})


@admin_bp.get("/admin/me")
@require_admin
def get_admin_profile():
    return jsonify({"admin": g.current_admin.to_dict()})


@admin_bp.get("/admin/dashboard")
@require_admin
def get_admin_dashboard():
    return jsonify(
        {
            "counts": {
                "products": Product.query.count(),
                "categories": Category.query.count(),
                "orders": Order.query.count(),
                "users": User.query.count(),
                "messages": ContactMessage.query.count(),
            }
        }
    )


@admin_bp.get("/admin/categories")
@require_admin
def admin_list_categories():
    categories = Category.query.order_by(Category.name.asc()).all()
    return jsonify({"items": [category.to_dict() for category in categories]})


@admin_bp.post("/admin/categories")
@require_admin
def admin_create_category():
    payload = request.get_json(silent=True) or {}

    name = (payload.get("name") or "").strip()
    if not name:
        return jsonify({"error": "Category name is required"}), 400

    slug = _slugify(payload.get("slug") or name)
    if not slug:
        return jsonify({"error": "Invalid category slug"}), 400

    existing = Category.query.filter_by(slug=slug).first()
    if existing:
        return jsonify({"error": "Category already exists"}), 409

    category = Category(
        name=name,
        slug=slug,
        description=(payload.get("description") or "").strip() or None,
    )
    db.session.add(category)
    db.session.commit()

    return jsonify({"message": "Category created", "category": category.to_dict()}), 201


@admin_bp.get("/admin/products")
@require_admin
def admin_list_products():
    page = max(request.args.get("page", 1, type=int), 1)
    per_page = max(1, min(request.args.get("per_page", 20, type=int), 50))

    pagination = Product.query.order_by(Product.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False,
    )

    return jsonify(
        {
            "items": [item.to_dict() for item in pagination.items],
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "pages": pagination.pages,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev,
            },
        }
    )


@admin_bp.post("/admin/products")
@require_admin
def admin_create_product():
    payload = request.get_json(silent=True) or {}

    try:
        product_data, error = _validate_create_product_payload(payload)
        if error:
            db.session.rollback()
            return jsonify({"error": error}), 400

        product = Product(**product_data)
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product created", "product": product.to_dict()}), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Could not create product"}), 500


@admin_bp.put("/admin/products/<int:product_id>")
@admin_bp.patch("/admin/products/<int:product_id>")
@require_admin
def admin_update_product(product_id):
    payload = request.get_json(silent=True) or {}
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    try:
        if "name" in payload:
            name = (payload.get("name") or "").strip()
            if not name:
                return jsonify({"error": "name cannot be empty"}), 400
            product.name = name

        if "short_description" in payload:
            value = (payload.get("short_description") or "").strip()
            if not value:
                return jsonify({"error": "short_description cannot be empty"}), 400
            product.short_description = value

        if "description" in payload:
            value = (payload.get("description") or "").strip()
            if not value:
                return jsonify({"error": "description cannot be empty"}), 400
            product.description = value

        if "scent" in payload:
            value = (payload.get("scent") or "").strip()
            if not value:
                return jsonify({"error": "scent cannot be empty"}), 400
            product.scent = value

        if "size" in payload:
            value = (payload.get("size") or "").strip()
            if not value:
                return jsonify({"error": "size cannot be empty"}), 400
            product.size = value

        if "burn_time" in payload:
            value = (payload.get("burn_time") or "").strip()
            if not value:
                return jsonify({"error": "burn_time cannot be empty"}), 400
            product.burn_time = value

        if "price" in payload:
            product.price = _to_decimal(payload.get("price"))

        if "inventory_count" in payload:
            inventory_count = _to_int(payload.get("inventory_count"))
            if inventory_count < 0:
                return jsonify({"error": "inventory_count cannot be negative"}), 400
            product.inventory_count = inventory_count

        if "featured" in payload:
            product.featured = bool(payload.get("featured"))

        if any(
            key in payload
            for key in ["category_id", "category_slug", "category", "category_name", "category_description"]
        ):
            category, category_error = _resolve_category(payload)
            if category_error:
                return jsonify({"error": category_error}), 400
            product.category_id = category.id

        if "images" in payload or "image" in payload or "image_url" in payload:
            product.images = _to_string_list(
                payload.get("images") or payload.get("image") or payload.get("image_url")
            )

        if "materials" in payload:
            product.materials = _to_string_list(payload.get("materials"))

        if "slug" in payload or "name" in payload:
            slug_input = (payload.get("slug") or product.name or "").strip()
            slug = _slugify(slug_input)
            if not slug:
                return jsonify({"error": "Invalid slug"}), 400
            product.slug = _ensure_unique_product_slug(slug, current_product_id=product.id)

        db.session.commit()
        return jsonify({"message": "Product updated", "product": product.to_dict()})
    except (TypeError, ValueError, InvalidOperation):
        db.session.rollback()
        return jsonify({"error": "Invalid product payload"}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Could not update product"}), 500


@admin_bp.delete("/admin/products/<int:product_id>")
@require_admin
def admin_delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"})


@admin_bp.get("/admin/orders")
@require_admin
def admin_list_orders():
    page = max(request.args.get("page", 1, type=int), 1)
    per_page = max(1, min(request.args.get("per_page", 20, type=int), 50))

    pagination = Order.query.order_by(Order.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False,
    )

    return jsonify(
        {
            "items": [order.to_dict() for order in pagination.items],
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "pages": pagination.pages,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev,
            },
        }
    )


@admin_bp.patch("/admin/orders/<int:order_id>/status")
@require_admin
def admin_update_order_status(order_id):
    payload = request.get_json(silent=True) or {}
    status = (payload.get("status") or "").strip().lower()

    if status not in ORDER_STATUSES:
        return jsonify({"error": "Invalid order status"}), 400

    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    order.status = status
    db.session.commit()
    return jsonify({"message": "Order status updated", "order": order.to_dict()})


@admin_bp.get("/admin/users")
@require_admin
def admin_list_users():
    limit = max(1, min(request.args.get("limit", 100, type=int), 300))
    users = User.query.order_by(User.created_at.desc()).limit(limit).all()
    return jsonify({"items": [user.to_dict() for user in users]})


@admin_bp.get("/admin/messages")
@require_admin
def admin_list_messages():
    limit = max(1, min(request.args.get("limit", 100, type=int), 300))
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(limit).all()
    return jsonify({"items": [message.to_dict() for message in messages]})
