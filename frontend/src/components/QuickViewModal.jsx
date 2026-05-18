import { useEffect } from "react";
import { Link } from "react-router-dom";

function QuickViewModal({ product, onClose, onAddToCart }) {
  useEffect(() => {
    if (!product) {
      return undefined;
    }

    const onKeydown = (event) => {
      if (event.key === "Escape") {
        onClose();
      }
    };

    document.body.style.overflow = "hidden";
    window.addEventListener("keydown", onKeydown);

    return () => {
      document.body.style.overflow = "";
      window.removeEventListener("keydown", onKeydown);
    };
  }, [product, onClose]);

  if (!product) {
    return null;
  }

  return (
    <div className="quick-view-overlay" onClick={onClose} role="presentation">
      <section className="quick-view-modal" onClick={(event) => event.stopPropagation()}>
        <button className="quick-view-close" type="button" onClick={onClose} aria-label="Close">
          ×
        </button>

        <img src={product.image} alt={product.name} className="quick-view-image" width="640" height="800" />

        <div className="quick-view-content">
          <p className="eyebrow">{product.category_name}</p>
          <h3>{product.name}</h3>
          <p>{product.short_description}</p>
          <ul>
            <li>Scent: {product.scent}</li>
            <li>Burn time: {product.burn_time}</li>
            <li>Size: {product.size}</li>
          </ul>
          <p className="price">${product.price.toFixed(2)}</p>

          <div className="quick-view-actions">
            <button type="button" className="primary-button" onClick={() => onAddToCart(product)}>
              Add To Cart
            </button>
            <Link to={`/shop/${product.slug}`} className="secondary-button" onClick={onClose}>
              Full Details
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}

export default QuickViewModal;
