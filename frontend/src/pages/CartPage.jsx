import { useState } from "react";
import { Link } from "react-router-dom";

import { api } from "../api/client";
import { useCart } from "../context/CartContext";

function CartPage() {
  const { items, subtotal, updateQuantity, removeItem, clearCart } = useCart();

  const [checkout, setCheckout] = useState({ name: "", email: "", marketing_opt_in: false });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [order, setOrder] = useState(null);

  const shippingFee = subtotal >= 120 || subtotal === 0 ? 0 : 12;
  const total = subtotal + shippingFee;

  const handlePlaceOrder = async (event) => {
    event.preventDefault();
    setError("");

    if (items.length === 0) {
      setError("Your cart is currently empty.");
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await api.createOrder({
        customer: checkout,
        items: items.map((item) => ({
          product_id: item.id,
          quantity: item.quantity,
        })),
      });

      setOrder(response.order);
      clearCart();
      setCheckout({ name: "", email: "", marketing_opt_in: false });
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (order) {
    return (
      <div className="page container section">
        <div className="success-card">
          <p className="eyebrow">Order Confirmed</p>
          <h1>Thank You For Your Order</h1>
          <p>Your order number is #{order.id}. A confirmation has been sent to {order.customer_email}.</p>
          <p>Total paid: ${order.total.toFixed(2)}</p>
          <Link to="/shop" className="primary-button">
            Continue Shopping
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="page container section cart-page">
      <div className="section-header">
        <p className="eyebrow">Cart</p>
        <h1>Your Selection</h1>
      </div>

      {items.length === 0 ? (
        <div className="empty-state">
          <h3>Your cart is empty</h3>
          <p>Explore our signature candle collection to begin your order.</p>
          <Link to="/shop" className="primary-button">
            Shop Candles
          </Link>
        </div>
      ) : (
        <div className="cart-layout">
          <div className="cart-items">
            {items.map((item) => (
              <article key={item.id} className="cart-item">
                <img src={item.image} alt={item.name} width="140" height="170" loading="lazy" />
                <div>
                  <h3>{item.name}</h3>
                  <p className="price">${item.price.toFixed(2)}</p>
                  <div className="cart-item-actions">
                    <label htmlFor={`quantity-${item.id}`}>Qty</label>
                    <input
                      id={`quantity-${item.id}`}
                      type="number"
                      min="1"
                      max={item.inventory_count || 99}
                      value={item.quantity}
                      onChange={(event) => updateQuantity(item.id, Number(event.target.value))}
                    />
                    <button type="button" onClick={() => removeItem(item.id)}>
                      Remove
                    </button>
                  </div>
                </div>
              </article>
            ))}
          </div>

          <aside className="cart-summary">
            <h3>Order Summary</h3>
            <div className="summary-row">
              <span>Subtotal</span>
              <span>${subtotal.toFixed(2)}</span>
            </div>
            <div className="summary-row">
              <span>Shipping</span>
              <span>{shippingFee === 0 ? "Free" : `$${shippingFee.toFixed(2)}`}</span>
            </div>
            <div className="summary-row total">
              <span>Total</span>
              <span>${total.toFixed(2)}</span>
            </div>

            <form className="checkout-form" onSubmit={handlePlaceOrder}>
              <label>
                Full Name
                <input
                  type="text"
                  value={checkout.name}
                  onChange={(event) =>
                    setCheckout((current) => ({ ...current, name: event.target.value }))
                  }
                  required
                />
              </label>
              <label>
                Email
                <input
                  type="email"
                  value={checkout.email}
                  onChange={(event) =>
                    setCheckout((current) => ({ ...current, email: event.target.value }))
                  }
                  required
                />
              </label>

              <label className="checkbox-row">
                <input
                  type="checkbox"
                  checked={checkout.marketing_opt_in}
                  onChange={(event) =>
                    setCheckout((current) => ({
                      ...current,
                      marketing_opt_in: event.target.checked,
                    }))
                  }
                />
                Keep me updated with new launches
              </label>

              {error && <p className="error-text">{error}</p>}

              <button className="primary-button" type="submit" disabled={isSubmitting}>
                {isSubmitting ? "Placing Order..." : "Place Order"}
              </button>
            </form>
          </aside>
        </div>
      )}
    </div>
  );
}

export default CartPage;
