import { useState } from "react";

import { api } from "../api/client";

function ContactPage() {
  const [formData, setFormData] = useState({ name: "", email: "", message: "" });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [status, setStatus] = useState({ type: "", message: "" });

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((current) => ({ ...current, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsSubmitting(true);
    setStatus({ type: "", message: "" });

    try {
      await api.createContactMessage({
        name: formData.name,
        email: formData.email,
        message: formData.message,
      });

      setStatus({
        type: "success",
        message: "Thank you. We received your message and will get back to you soon.",
      });
      setFormData({ name: "", email: "", message: "" });
    } catch (error) {
      setStatus({ type: "error", message: error.message });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="page container section contact-page">
      <div className="section-header">
        <p className="eyebrow">Contact</p>
        <h1>Let Us Build Your Signature Ambiance</h1>
        <p className="muted">For wholesale, collaborations, and general inquiries, send us a message.</p>
      </div>

      <div className="contact-layout">
        <form className="contact-form" onSubmit={handleSubmit}>
          <label>
            Name
            <input type="text" name="name" value={formData.name} onChange={handleChange} required />
          </label>

          <label>
            Email
            <input type="email" name="email" value={formData.email} onChange={handleChange} required />
          </label>

          <label>
            Message
            <textarea
              name="message"
              rows="5"
              value={formData.message}
              onChange={handleChange}
              required
            />
          </label>

          <button type="submit" className="primary-button" disabled={isSubmitting}>
            {isSubmitting ? "Sending..." : "Send Message"}
          </button>

          {status.message && (
            <p className={`form-status ${status.type === "error" ? "error" : "success"}`}>
              {status.message}
            </p>
          )}
        </form>

        <aside className="contact-meta">
          <h3>Connect With Us</h3>
          <p>Email: hello@efpstore.com</p>
          <p>Instagram: @efpstore</p>
          <p>Pinterest: EFP</p>
          <p>TikTok: @efpstore</p>
        </aside>
      </div>
    </div>
  );
}

export default ContactPage;
