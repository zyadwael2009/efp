import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { api } from "../api/client";
import ProductCard from "../components/ProductCard";
import { useCart } from "../context/CartContext";

function HomePage() {
  const { addItem } = useCart();
  const [featured, setFeatured] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadFeatured = async () => {
      try {
        const response = await api.getProducts({ featured: true, per_page: 4, sort: "featured" });
        setFeatured(response.items || []);
      } catch (requestError) {
        setError(requestError.message);
      } finally {
        setLoading(false);
      }
    };

    loadFeatured();
  }, []);

  return (
    <div className="page home-page">
      <section className="hero container">
        <div className="hero-content fade-up">
          <p className="eyebrow">Handcrafted Atmosphere</p>
          <h1>Light Your Space with Elegance</h1>
          <p>
            Minimal forms. Premium scents. A calm, elevated collection designed to transform everyday
            routines into intentional rituals.
          </p>
          <div className="hero-actions">
            <Link to="/shop" className="primary-button">
              Shop Now
            </Link>
            <Link to="/about" className="secondary-button">
              Explore
            </Link>
          </div>
        </div>

        <div className="hero-card fade-up">
          <h3>Designed To Grow</h3>
          <p>
            Today: artisanal candles. Tomorrow: home decor, fragrances, and gifts under one premium
            brand ecosystem.
          </p>
          <Link to="/shop" className="inline-link">
            Browse the current collection
          </Link>
        </div>
      </section>

      <section className="section container">
        <div className="section-header">
          <p className="eyebrow">Featured Candles</p>
          <h2>Signature Picks</h2>
        </div>

        {loading && <p className="muted">Loading featured products...</p>}
        {error && <p className="error-text">{error}</p>}

        {!loading && !error && featured.length === 0 && (
          <p className="muted">No featured products yet. Add some from the admin catalog when you are ready.</p>
        )}

        {!loading && !error && featured.length > 0 && (
          <div className="product-grid">
            {featured.map((product) => (
              <ProductCard key={product.id} product={product} onAddToCart={addItem} />
            ))}
          </div>
        )}
      </section>

      <section className="section container split-section">
        <div className="fade-up">
          <p className="eyebrow">Brand Story</p>
          <h2>Handmade With Precision, Built With Vision</h2>
          <p>
            Every candle is hand-poured in small batches with a focus on quality ingredients and
            timeless design. We build around calm, comfort, and intention.
          </p>
          <p>
            The platform architecture already supports expansion into adjacent categories, keeping your
            future growth straightforward and scalable.
          </p>
          <Link to="/about" className="secondary-button">
            Read Our Story
          </Link>
        </div>

        <div className="future-grid fade-up">
          <article>
            <h4>Home Decor</h4>
            <p>Sculptural accents that align with your fragrance rituals.</p>
          </article>
          <article>
            <h4>Fragrances</h4>
            <p>Diffusers and room sprays for layered scent experiences.</p>
          </article>
          <article>
            <h4>Gift Sets</h4>
            <p>Curated bundles for seasonal launches and special occasions.</p>
          </article>
        </div>
      </section>
    </div>
  );
}

export default HomePage;
