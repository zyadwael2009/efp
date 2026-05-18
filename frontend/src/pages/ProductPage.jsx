import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { api } from "../api/client";
import ProductCard from "../components/ProductCard";
import { useCart } from "../context/CartContext";

function ProductPage() {
  const { identifier } = useParams();
  const { addItem } = useCart();

  const [product, setProduct] = useState(null);
  const [relatedProducts, setRelatedProducts] = useState([]);
  const [selectedImage, setSelectedImage] = useState("");
  const [quantity, setQuantity] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadProduct = async () => {
      setLoading(true);
      setError("");

      try {
        const result = await api.getProduct(identifier);
        setProduct(result);
        setSelectedImage(result.images?.[0] || "");

        const related = await api.getProducts({
          category: result.category,
          per_page: 4,
          sort: "featured",
        });

        setRelatedProducts((related.items || []).filter((item) => item.id !== result.id).slice(0, 3));
      } catch (requestError) {
        setError(requestError.message);
      } finally {
        setLoading(false);
      }
    };

    loadProduct();
  }, [identifier]);

  if (loading) {
    return (
      <div className="page container section">
        <p className="muted">Loading product details...</p>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="page container section">
        <p className="error-text">{error || "Product not found"}</p>
        <Link to="/shop" className="secondary-button">
          Back To Shop
        </Link>
      </div>
    );
  }

  const maxQuantity = Math.max(1, Math.min(product.inventory_count, 10));

  return (
    <div className="page container section">
      <div className="product-detail-layout">
        <div>
          <div className="product-main-image-wrap">
            <img
              src={selectedImage || product.image}
              alt={product.name}
              className="product-main-image"
              width="900"
              height="1100"
            />
          </div>

          <div className="thumbnail-row">
            {product.images?.map((image) => (
              <button
                type="button"
                key={image}
                className={`thumbnail-button ${selectedImage === image ? "active" : ""}`}
                onClick={() => setSelectedImage(image)}
              >
                <img src={image} alt={`${product.name} thumbnail`} width="180" height="220" />
              </button>
            ))}
          </div>
        </div>

        <div className="product-info">
          <p className="eyebrow">{product.category_name}</p>
          <h1>{product.name}</h1>
          <p className="price">${product.price.toFixed(2)}</p>
          <p>{product.description}</p>

          <div className="product-specs">
            <div>
              <h4>Scent</h4>
              <p>{product.scent}</p>
            </div>
            <div>
              <h4>Burn Time</h4>
              <p>{product.burn_time}</p>
            </div>
            <div>
              <h4>Size</h4>
              <p>{product.size}</p>
            </div>
            <div>
              <h4>Materials</h4>
              <p>{product.materials?.join(", ")}</p>
            </div>
          </div>

          <div className="quantity-row">
            <label htmlFor="quantity">Quantity</label>
            <input
              id="quantity"
              type="number"
              min="1"
              max={maxQuantity}
              value={quantity}
              onChange={(event) => setQuantity(Number(event.target.value))}
            />
          </div>

          <button
            type="button"
            className="primary-button"
            onClick={() => addItem(product, quantity)}
            disabled={product.inventory_count <= 0}
          >
            {product.inventory_count > 0 ? "Add To Cart" : "Out Of Stock"}
          </button>

          <p className="muted">{product.inventory_count} in stock</p>
        </div>
      </div>

      <section className="section reviews-section">
        <div className="section-header">
          <p className="eyebrow">Reviews</p>
          <h2>What Customers Say</h2>
        </div>

        {product.reviews?.length ? (
          <div className="reviews-grid">
            {product.reviews.map((review) => (
              <article key={review.id} className="review-card">
                <h4>{review.title}</h4>
                <p className="muted">{review.author}</p>
                <p>{review.comment}</p>
                <p className="muted">Rating: {review.rating}/5</p>
              </article>
            ))}
          </div>
        ) : (
          <p className="muted">No reviews yet.</p>
        )}
      </section>

      {relatedProducts.length > 0 && (
        <section className="section">
          <div className="section-header">
            <p className="eyebrow">You May Also Like</p>
            <h2>Related Picks</h2>
          </div>

          <div className="product-grid">
            {relatedProducts.map((relatedProduct) => (
              <ProductCard key={relatedProduct.id} product={relatedProduct} onAddToCart={addItem} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

export default ProductPage;
