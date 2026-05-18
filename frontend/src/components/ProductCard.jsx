import { Link } from "react-router-dom";

function ProductCard({ product, onQuickView, onAddToCart }) {
  return (
    <article className="product-card fade-up">
      <Link to={`/shop/${product.slug}`} className="product-image-wrapper" aria-label={product.name}>
        <img
          src={product.image}
          alt={product.name}
          loading="lazy"
          width="640"
          height="800"
          className="product-image"
        />
      </Link>

      <div className="product-content">
        <p className="product-category">{product.category_name}</p>
        <h3>
          <Link to={`/shop/${product.slug}`}>{product.name}</Link>
        </h3>
        <p className="product-description">{product.short_description}</p>
        <div className="product-meta">
          <span>{product.scent}</span>
          <span>{product.size}</span>
        </div>
        <div className="product-footer">
          <span className="price">${product.price.toFixed(2)}</span>
          <div className="product-actions">
            <button type="button" onClick={() => onQuickView?.(product)}>
              Quick View
            </button>
            <button type="button" onClick={() => onAddToCart(product)}>
              Add
            </button>
          </div>
        </div>
      </div>
    </article>
  );
}

export default ProductCard;
