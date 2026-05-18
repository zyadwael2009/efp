import { useState } from "react";
import { Link } from "react-router-dom";

import { api } from "../api/client";

function RegisterPage() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    marketing_opt_in: true,
  });
  const [status, setStatus] = useState({ type: "", message: "" });

  const onSubmit = async (event) => {
    event.preventDefault();
    setStatus({ type: "", message: "" });

    try {
      await api.createOrUpdateUser({
        name: form.name.trim(),
        email: form.email.trim().toLowerCase(),
        marketing_opt_in: form.marketing_opt_in,
      });
      setStatus({
        type: "success",
        message: "You are registered. We will use your email for orders and updates you opt into.",
      });
      setForm({ name: "", email: "", marketing_opt_in: true });
    } catch (error) {
      setStatus({ type: "error", message: error.message });
    }
  };

  return (
    <div className="page container section">
      <div className="section-header">
        <p className="eyebrow">Account</p>
        <h1>Create your profile</h1>
        <p className="muted">
          Register with your name and email so checkout and newsletters stay in sync. This is not the
          store admin login.
        </p>
      </div>

      <form className="contact-form" style={{ maxWidth: "28rem" }} onSubmit={onSubmit}>
        <label>
          Name
          <input
            type="text"
            value={form.name}
            onChange={(event) => setForm((current) => ({ ...current, name: event.target.value }))}
            required
          />
        </label>
        <label>
          Email
          <input
            type="email"
            value={form.email}
            onChange={(event) => setForm((current) => ({ ...current, email: event.target.value }))}
            required
          />
        </label>
        <label className="checkbox-row">
          <input
            type="checkbox"
            checked={form.marketing_opt_in}
            onChange={(event) =>
              setForm((current) => ({ ...current, marketing_opt_in: event.target.checked }))
            }
          />
          <span>Email me about new products and offers</span>
        </label>
        <button type="submit" className="primary-button">
          Register
        </button>
        {status.message && (
          <p className={`form-status ${status.type === "error" ? "error" : "success"}`}>
            {status.message}
          </p>
        )}
        <p className="muted">
          Store staff? Open the{" "}
          <Link to="/admin" className="inline-link">
            admin login
          </Link>{" "}
          in a separate tab.
        </p>
      </form>
    </div>
  );
}

export default RegisterPage;
