import { useState } from "react";
import { Link } from "react-router-dom";

import { api } from "../api/client";

function Footer() {
  const [formState, setFormState] = useState({ name: "", email: "" });
  const [status, setStatus] = useState({ type: "", message: "" });

  const handleSubmit = async (event) => {
    event.preventDefault();
    setStatus({ type: "", message: "" });

    try {
      await api.createOrUpdateUser({
        name: formState.name,
        email: formState.email,
        marketing_opt_in: true,
      });

      setStatus({
        type: "success",
        message: "Subscribed. We will share new drops and launch news.",
      });
      setFormState({ name: "", email: "" });
    } catch (error) {
      setStatus({ type: "error", message: error.message });
    }
  };

  return (
    <footer className="footer">
      <div className="container footer-grid">
        <div>
          <h3 className="footer-brand">EFP</h3>
          <p className="footer-text">
            Handcrafted essentials for calm interiors. Built to grow from candles to a full lifestyle
            collection.
          </p>
          <div className="social-links">
            <a href="https://instagram.com" target="_blank" rel="noreferrer">
              Instagram
            </a>
            <a href="https://pinterest.com" target="_blank" rel="noreferrer">
              Pinterest
            </a>
            <a href="https://tiktok.com" target="_blank" rel="noreferrer">
              TikTok
            </a>
          </div>
        </div>

        <div>
          <h4>Navigate</h4>
          <div className="footer-links">
            <Link to="/">Home</Link>
            <Link to="/shop">Shop</Link>
            <Link to="/about">About</Link>
            <Link to="/contact">Contact</Link>
            <Link to="/register">Register</Link>
          </div>
        </div>

        <div>
          <h4>Join The List</h4>
          <form className="newsletter-form" onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Name"
              value={formState.name}
              onChange={(event) =>
                setFormState((current) => ({ ...current, name: event.target.value }))
              }
              required
            />
            <input
              type="email"
              placeholder="Email"
              value={formState.email}
              onChange={(event) =>
                setFormState((current) => ({ ...current, email: event.target.value }))
              }
              required
            />
            <button type="submit">Subscribe</button>
          </form>
          {status.message && (
            <p className={`form-status ${status.type === "error" ? "error" : "success"}`}>
              {status.message}
            </p>
          )}
        </div>
      </div>

      <div className="footer-bottom">
        <p>© {new Date().getFullYear()} EFP. All rights reserved.</p>
      </div>
    </footer>
  );
}

export default Footer;
