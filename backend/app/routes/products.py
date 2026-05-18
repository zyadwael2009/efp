from flask import Blueprint, jsonify, request
from sqlalchemy import desc, or_

from ..models import Category, Product


products_bp = Blueprint("products", __name__)


@products_bp.get("/products")
def list_products():
    query = Product.query

    category = request.args.get("category")
    if category:
        query = query.join(Category).filter(Category.slug == category)

    scent = request.args.get("scent")
    if scent:
        query = query.filter(Product.scent.ilike(f"%{scent}%"))

    size = request.args.get("size")
    if size:
        query = query.filter(Product.size.ilike(size))

    min_price = request.args.get("min_price", type=float)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    max_price = request.args.get("max_price", type=float)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    featured = request.args.get("featured")
    if featured and featured.lower() in {"1", "true", "yes"}:
        query = query.filter(Product.featured.is_(True))

    search = request.args.get("search")
    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%"),
                Product.short_description.ilike(f"%{search}%"),
            )
        )

    sort = request.args.get("sort", "featured")
    if sort == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort == "price_desc":
        query = query.order_by(Product.price.desc())
    elif sort == "newest":
        query = query.order_by(desc(Product.created_at))
    else:
        query = query.order_by(desc(Product.featured), desc(Product.created_at))

    page = max(request.args.get("page", 1, type=int), 1)
    per_page = request.args.get("per_page", 12, type=int)
    per_page = max(1, min(per_page, 40))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify(
        {
            "items": [product.to_dict() for product in pagination.items],
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


@products_bp.get("/products/<string:identifier>")
def get_product(identifier):
    if identifier.isdigit():
        product = Product.query.get(int(identifier))
    else:
        product = Product.query.filter_by(slug=identifier).first()

    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product.to_dict(include_reviews=True))


@products_bp.get("/categories")
def list_categories():
    categories = Category.query.order_by(Category.name.asc()).all()
    return jsonify({"items": [category.to_dict() for category in categories]})
