from decimal import Decimal, InvalidOperation

from flask import Blueprint, jsonify, request

from ..extensions import db
from ..models import Order, OrderItem, Product, User


orders_bp = Blueprint("orders", __name__)


def _to_decimal(value):
    return Decimal(str(value)).quantize(Decimal("0.01"))


@orders_bp.get("/orders")
def list_orders():
    page = max(request.args.get("page", 1, type=int), 1)
    per_page = max(1, min(request.args.get("per_page", 20, type=int), 50))
    pagination = Order.query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify(
        {
            "items": [order.to_dict() for order in pagination.items],
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "pages": pagination.pages,
            },
        }
    )


@orders_bp.get("/orders/<int:order_id>")
def get_order(order_id):
    order = Order.query.get(order_id)

    if not order:
        return jsonify({"error": "Order not found"}), 404

    return jsonify(order.to_dict())


@orders_bp.post("/orders")
def create_order():
    payload = request.get_json(silent=True) or {}
    customer = payload.get("customer", {})
    raw_items = payload.get("items", [])

    customer_name = (customer.get("name") or "").strip()
    customer_email = (customer.get("email") or "").strip().lower()

    if not customer_name or not customer_email:
        return jsonify({"error": "Customer name and email are required"}), 400

    if not raw_items:
        return jsonify({"error": "At least one order item is required"}), 400

    order_lines = []
    subtotal = Decimal("0.00")

    try:
        for item in raw_items:
            product_id = int(item.get("product_id"))
            quantity = int(item.get("quantity", 1))

            if quantity < 1:
                raise ValueError("Quantity must be at least 1")

            product = Product.query.get(product_id)
            if not product:
                return jsonify({"error": f"Product {product_id} was not found"}), 404

            if product.inventory_count < quantity:
                return (
                    jsonify({"error": f"Not enough inventory for {product.name}"}),
                    409,
                )

            unit_price = _to_decimal(product.price)
            line_total = unit_price * quantity
            subtotal += line_total
            order_lines.append((product, quantity, unit_price))

        shipping_fee = Decimal("0.00") if subtotal >= Decimal("120.00") else Decimal("12.00")
        total = subtotal + shipping_fee

        user = User.query.filter_by(email=customer_email).first()
        if not user:
            user = User(
                name=customer_name,
                email=customer_email,
                marketing_opt_in=bool(customer.get("marketing_opt_in", False)),
            )
            db.session.add(user)
        else:
            user.name = customer_name

        order = Order(
            customer_name=customer_name,
            customer_email=customer_email,
            status="confirmed",
            subtotal=subtotal,
            shipping_fee=shipping_fee,
            total=total,
            user=user,
        )
        db.session.add(order)
        db.session.flush()

        for product, quantity, unit_price in order_lines:
            product.inventory_count -= quantity
            db.session.add(
                OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    product_name=product.name,
                    quantity=quantity,
                    unit_price=unit_price,
                )
            )

        db.session.commit()
        return jsonify({"message": "Order placed successfully", "order": order.to_dict()}), 201

    except (TypeError, ValueError, InvalidOperation):
        db.session.rollback()
        return jsonify({"error": "Invalid order payload"}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Could not process order"}), 500
