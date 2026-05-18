import { useState } from "react";
import { Link, NavLink } from "react-router-dom";

import { useCart } from "../context/CartContext";

const navLinks = [
  { to: "/", label: "Home" },
  { to: "/shop", label: "Shop" },
  { to: "/about", label: "About" },
  { to: "/contact", label: "Contact" },
  { to: "/register", label: "Register" },
];

function Navbar({ theme, onToggleTheme }) {
  const [isOpen, setIsOpen] = useState(false);
  const { totalItems } = useCart();

  return (
    <header className="navbar-wrapper">
      <nav className="navbar container">
        <button
          className="mobile-menu-toggle"
          type="button"
          aria-label="Toggle menu"
          onClick={() => setIsOpen((current) => !current)}
        >
          <span />
          <span />
        </button>

        <Link to="/" className="brand" onClick={() => setIsOpen(false)}>
          <span className="brand-mark">EFP</span>
          <span className="brand-sub">Store</span>
        </Link>

        <div className={`navbar-links ${isOpen ? "is-open" : ""}`}>
          {navLinks.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) => `navbar-link ${isActive ? "active" : ""}`}
              onClick={() => setIsOpen(false)}
            >
              {link.label}
            </NavLink>
          ))}
        </div>

        <div className="navbar-actions">
          <button type="button" className="theme-toggle" onClick={onToggleTheme}>
            {theme === "light" ? "Dark" : "Light"}
          </button>

          <Link to="/cart" className="cart-link">
            Cart
            <span className="cart-count">{totalItems}</span>
          </Link>
        </div>
      </nav>
    </header>
  );
}

export default Navbar;
