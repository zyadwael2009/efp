from datetime import datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


def utcnow():
    return datetime.now(timezone.utc)


class TimestampMixin:
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=utcnow,
        onupdate=utcnow,
        nullable=False,
    )


class Category(TimestampMixin, db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    slug = db.Column(db.String(80), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True)

    products = db.relationship("Product", back_populates="category", lazy="selectin")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "product_count": len(self.products),
        }


class Product(TimestampMixin, db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    slug = db.Column(db.String(140), nullable=False, unique=True, index=True)
    short_description = db.Column(db.String(220), nullable=False)
    description = db.Column(db.Text, nullable=False)
    scent = db.Column(db.String(80), nullable=False)
    size = db.Column(db.String(40), nullable=False)
    burn_time = db.Column(db.String(60), nullable=False)
    materials = db.Column(db.JSON, nullable=False, default=list)
    images = db.Column(db.JSON, nullable=False, default=list)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    featured = db.Column(db.Boolean, default=False, nullable=False)
    inventory_count = db.Column(db.Integer, nullable=False, default=0)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    category = db.relationship("Category", back_populates="products", lazy="joined")
    reviews = db.relationship(
        "Review",
        back_populates="product",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def rating(self):
        if not self.reviews:
            return 0
        return round(sum(review.rating for review in self.reviews) / len(self.reviews), 1)

    def to_dict(self, include_reviews=False):
        payload = {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "short_description": self.short_description,
            "description": self.description,
            "scent": self.scent,
            "size": self.size,
            "burn_time": self.burn_time,
            "materials": self.materials,
            "images": self.images,
            "image": self.images[0] if self.images else None,
            "price": float(self.price),
            "featured": self.featured,
            "inventory_count": self.inventory_count,
            "category": self.category.slug if self.category else None,
            "category_name": self.category.name if self.category else None,
            "rating": self.rating(),
            "review_count": len(self.reviews),
        }

        if include_reviews:
            payload["reviews"] = [review.to_dict() for review in self.reviews]

        return payload


class Review(TimestampMixin, db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    product = db.relationship("Product", back_populates="reviews", lazy="joined")

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "title": self.title,
            "comment": self.comment,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
        }


class Admin(TimestampMixin, db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(180), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    last_login_at = db.Column(db.DateTime(timezone=True), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
            "created_at": self.created_at.isoformat(),
        }


class User(TimestampMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(180), nullable=False, unique=True, index=True)
    marketing_opt_in = db.Column(db.Boolean, nullable=False, default=True)

    orders = db.relationship("Order", back_populates="user", lazy="selectin")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "marketing_opt_in": self.marketing_opt_in,
            "created_at": self.created_at.isoformat(),
        }


class ContactMessage(TimestampMixin, db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(180), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "message": self.message,
            "created_at": self.created_at.isoformat(),
        }


class Order(TimestampMixin, db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False, default="pending")
    customer_name = db.Column(db.String(120), nullable=False)
    customer_email = db.Column(db.String(180), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    shipping_fee = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    total = db.Column(db.Numeric(10, 2), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    user = db.relationship("User", back_populates="orders", lazy="joined")
    items = db.relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "customer_name": self.customer_name,
            "customer_email": self.customer_email,
            "subtotal": float(self.subtotal),
            "shipping_fee": float(self.shipping_fee),
            "total": float(self.total),
            "created_at": self.created_at.isoformat(),
            "items": [item.to_dict() for item in self.items],
        }


class OrderItem(TimestampMixin, db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(140), nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    order = db.relationship("Order", back_populates="items", lazy="joined")
    product = db.relationship("Product", lazy="joined")

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "unit_price": float(self.unit_price),
            "line_total": float(self.unit_price) * self.quantity,
        }
