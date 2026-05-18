import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

import { api } from "../api/client";

const ORDER_STATUSES = [
  "pending",
  "confirmed",
  "processing",
  "shipped",
  "delivered",
  "cancelled",
  "refunded",
];

const emptyProductForm = {
  name: "",
  category_name: "",
  short_description: "",
  description: "",
  scent: "",
  size: "",
  burn_time: "",
  price: "",
  inventory_count: "",
  image_url: "",
  materials: "",
  featured: false,
};

function parseList(value) {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function materialsToString(materials) {
  if (!materials) {
    return "";
  }
  if (Array.isArray(materials)) {
    return materials.join(", ");
  }
  return String(materials);
}

function AdminPage() {
  const [token, setToken] = useState(() => api.getAdminToken());
  const [admin, setAdmin] = useState(null);
  const [dashboard, setDashboard] = useState(null);
  const [products, setProducts] = useState([]);
  const [adminCategories, setAdminCategories] = useState([]);
  const [orders, setOrders] = useState([]);
  const [users, setUsers] = useState([]);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(Boolean(token));

  const [loginForm, setLoginForm] = useState({ email: "", password: "" });
  const [productForm, setProductForm] = useState(emptyProductForm);
  const [editingProductId, setEditingProductId] = useState(null);

  const [categoryForm, setCategoryForm] = useState({ name: "", slug: "", description: "" });

  const [status, setStatus] = useState({ type: "", message: "" });
  const [refreshKey, setRefreshKey] = useState(0);

  const metrics = useMemo(
    () => [
      { key: "products", label: "Products" },
      { key: "categories", label: "Categories" },
      { key: "orders", label: "Orders" },
      { key: "users", label: "Users" },
      { key: "messages", label: "Messages" },
    ],
    []
  );

  useEffect(() => {
    if (!adminCategories.length || editingProductId) {
      return;
    }
    setProductForm((prev) => {
      if (prev.category_name) {
        return prev;
      }
      return { ...prev, category_name: adminCategories[0].name };
    });
  }, [adminCategories, editingProductId]);

  useEffect(() => {
    if (!token) {
      setLoading(false);
      setAdmin(null);
      setDashboard(null);
      setProducts([]);
      setAdminCategories([]);
      setOrders([]);
      setUsers([]);
      setMessages([]);
      return;
    }

    let cancelled = false;

    async function loadAdminData() {
      setLoading(true);
      setStatus({ type: "", message: "" });

      try {
        const [adminRes, dashboardRes, productRes, catRes, orderRes, userRes, msgRes] = await Promise.all([
          api.getAdminProfile(token),
          api.getAdminDashboard(token),
          api.getAdminProducts({ page: 1, per_page: 100 }, token),
          api.getAdminCategories(token),
          api.getAdminOrders({ page: 1, per_page: 50 }, token),
          api.getAdminUsers({ limit: 200 }, token),
          api.getAdminMessages({ limit: 200 }, token),
        ]);

        if (cancelled) {
          return;
        }

        setAdmin(adminRes.admin || null);
        setDashboard(dashboardRes.counts || null);
        setProducts(productRes.items || []);
        setAdminCategories(catRes.items || []);
        setOrders(orderRes.items || []);
        setUsers(userRes.items || []);
        setMessages(msgRes.items || []);
      } catch (error) {
        if (cancelled) {
          return;
        }

        api.clearAdminToken();
        setToken("");
        setStatus({ type: "error", message: error.message || "Session expired. Please login again." });
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadAdminData();

    return () => {
      cancelled = true;
    };
  }, [token, refreshKey]);

  const resetProductForm = () => {
    const firstCat = adminCategories[0]?.name || "";
    setProductForm({ ...emptyProductForm, category_name: firstCat });
    setEditingProductId(null);
  };

  const onLogin = async (event) => {
    event.preventDefault();
    setStatus({ type: "", message: "" });

    try {
      const response = await api.adminLogin(loginForm);
      setToken(response.token || "");
      setStatus({ type: "success", message: "Logged in as admin." });
      setLoginForm({ email: "", password: "" });
    } catch (error) {
      setStatus({ type: "error", message: error.message });
    }
  };

  const buildProductPayload = () => ({
    ...productForm,
    price: Number(productForm.price),
    inventory_count: Number(productForm.inventory_count || 0),
    materials: parseList(productForm.materials),
  });

  const onSaveProduct = async (event) => {
    event.preventDefault();
    setStatus({ type: "", message: "" });

    try {
      const payload = buildProductPayload();
      if (editingProductId) {
        await api.patchAdminProduct(editingProductId, payload, token);
        setStatus({ type: "success", message: "Product updated." });
      } else {
        await api.createAdminProduct(payload, token);
        setStatus({ type: "success", message: "Product created." });
      }
      resetProductForm();
      setRefreshKey((current) => current + 1);
    } catch (error) {
      setStatus({ type: "error", message: error.message });
    }
  };

  const onDeleteProduct = async (productId) => {
    setStatus({ type: "", message: "" });

    try {
      await api.deleteAdminProduct(productId, token);
      if (editingProductId === productId) {
        resetProductForm();
      }
      setProducts((current) => current.filter((item) => item.id !== productId));
      setStatus({ type: "success", message: "Product deleted." });
      setRefreshKey((current) => current + 1);
    } catch (error) {
      setStatus({ type: "error", message: error.message });
    }
  };

  const onStartEditProduct = (product) => {
    setEditingProductId(product.id);
    setProductForm({
      name: product.name || "",
      category_name: product.category_name || adminCategories[0]?.name || "",
      short_description: product.short_description || "",
      description: product.description || "",
      scent: product.scent || "",
      size: product.size || "",
      burn_time: product.burn_time || "",
      price: String(product.price ?? ""),
      inventory_count: String(product.inventory_count ?? 0),
      image_url: product.images?.[0] || product.image || "",
      materials: materialsToString(product.materials),
      featured: Boolean(product.featured),
    });
  };

  const onCreateCategory = async (event) => {
    event.preventDefault();
    setStatus({ type: "", message: "" });

    try {
      const catPayload = { name: categoryForm.name.trim() };
      const slug = categoryForm.slug.trim();
      const desc = categoryForm.description.trim();
      if (slug) {
        catPayload.slug = slug;
      }
      if (desc) {
        catPayload.description = desc;
      }
      await api.createAdminCategory(catPayload, token);
      setCategoryForm({ name: "", slug: "", description: "" });
      setStatus({ type: "success", message: "Category created." });
      setRefreshKey((current) => current + 1);
    } catch (error) {
      setStatus({ type: "error", message: error.message });
    }
  };

  const onOrderStatusChange = async (orderId, status) => {
    setStatus({ type: "", message: "" });
    try {
      await api.updateAdminOrderStatus(orderId, status, token);
      setOrders((current) =>
        current.map((order) => (order.id === orderId ? { ...order, status } : order))
      );
      setStatus({ type: "success", message: "Order status updated." });
      setRefreshKey((current) => current + 1);
    } catch (error) {
      setStatus({ type: "error", message: error.message });
    }
  };

  const onLogout = () => {
    api.clearAdminToken();
    setToken("");
    resetProductForm();
    setStatus({ type: "success", message: "Logged out." });
  };

  if (!token) {
    return (
      <div className="admin-shell-inner">
        <header className="admin-top-bar">
          <Link to="/" className="inline-link">
            ← Back to store
          </Link>
        </header>
        <div className="page container section admin-page">
          <div className="section-header">
            <p className="eyebrow">EFP Admin</p>
            <h1>Staff login</h1>
            <p className="muted">Sign in to manage catalog, orders, and customer messages.</p>
            {status.message && (
              <p className={`form-status ${status.type === "error" ? "error" : "success"}`}>
                {status.message}
              </p>
            )}
          </div>

          <form className="admin-card admin-login-only" onSubmit={onLogin}>
            <h3>Admin login</h3>
            <label>
              Email
              <input
                type="email"
                value={loginForm.email}
                onChange={(event) =>
                  setLoginForm((current) => ({ ...current, email: event.target.value }))
                }
                required
              />
            </label>
            <label>
              Password
              <input
                type="password"
                value={loginForm.password}
                onChange={(event) =>
                  setLoginForm((current) => ({ ...current, password: event.target.value }))
                }
                required
              />
            </label>
            <button type="submit" className="primary-button">
              Login
            </button>
            <p className="muted small-print">
              Customer registration lives on the{" "}
              <Link to="/register" className="inline-link">
                Register
              </Link>{" "}
              page.
            </p>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="admin-shell-inner">
      <header className="admin-top-bar">
        <Link to="/" className="inline-link">
          ← Back to store
        </Link>
        <span className="muted" style={{ fontSize: "0.9rem" }}>
          Admin console
        </span>
      </header>

      <div className="page container section admin-page">
        <div className="section-header admin-heading">
          <div>
            <p className="eyebrow">EFP Admin</p>
            <h1>Welcome, {admin?.name || "Admin"}</h1>
            <p className="muted">Catalog, orders, categories, users, and inbox.</p>
          </div>
          <button type="button" className="secondary-button" onClick={onLogout}>
            Logout
          </button>
        </div>

        {status.message && (
          <p className={`form-status ${status.type === "error" ? "error" : "success"}`}>{status.message}</p>
        )}

        {loading ? (
          <p className="muted">Loading admin data...</p>
        ) : (
          <>
            <section className="admin-metric-grid">
              {metrics.map((metric) => (
                <article key={metric.key} className="admin-metric-card">
                  <p>{metric.label}</p>
                  <h3>{dashboard?.[metric.key] ?? 0}</h3>
                </article>
              ))}
            </section>

            <section className="admin-layout admin-layout--stack">
              <form className="admin-card" onSubmit={onSaveProduct}>
                <h3>{editingProductId ? "Edit product" : "Add product"}</h3>
                <label>
                  Name
                  <input
                    type="text"
                    value={productForm.name}
                    onChange={(event) =>
                      setProductForm((current) => ({ ...current, name: event.target.value }))
                    }
                    required
                  />
                </label>

                <label>
                  Category name
                  <input
                    type="text"
                    value={productForm.category_name}
                    onChange={(event) =>
                      setProductForm((current) => ({ ...current, category_name: event.target.value }))
                    }
                    required
                  />
                </label>

                <label>
                  Short description
                  <input
                    type="text"
                    value={productForm.short_description}
                    onChange={(event) =>
                      setProductForm((current) => ({ ...current, short_description: event.target.value }))
                    }
                    required
                  />
                </label>

                <label>
                  Description
                  <textarea
                    rows="4"
                    value={productForm.description}
                    onChange={(event) =>
                      setProductForm((current) => ({ ...current, description: event.target.value }))
                    }
                    required
                  />
                </label>

                <div className="admin-grid-2">
                  <label>
                    Scent
                    <input
                      type="text"
                      value={productForm.scent}
                      onChange={(event) =>
                        setProductForm((current) => ({ ...current, scent: event.target.value }))
                      }
                      required
                    />
                  </label>

                  <label>
                    Size
                    <input
                      type="text"
                      value={productForm.size}
                      onChange={(event) =>
                        setProductForm((current) => ({ ...current, size: event.target.value }))
                      }
                      required
                    />
                  </label>
                </div>

                <div className="admin-grid-2">
                  <label>
                    Burn time
                    <input
                      type="text"
                      value={productForm.burn_time}
                      onChange={(event) =>
                        setProductForm((current) => ({ ...current, burn_time: event.target.value }))
                      }
                      required
                    />
                  </label>

                  <label>
                    Price
                    <input
                      type="number"
                      min="0"
                      step="0.01"
                      value={productForm.price}
                      onChange={(event) =>
                        setProductForm((current) => ({ ...current, price: event.target.value }))
                      }
                      required
                    />
                  </label>
                </div>

                <div className="admin-grid-2">
                  <label>
                    Inventory count
                    <input
                      type="number"
                      min="0"
                      value={productForm.inventory_count}
                      onChange={(event) =>
                        setProductForm((current) => ({ ...current, inventory_count: event.target.value }))
                      }
                      required
                    />
                  </label>

                  <label>
                    Featured
                    <select
                      value={productForm.featured ? "yes" : "no"}
                      onChange={(event) =>
                        setProductForm((current) => ({
                          ...current,
                          featured: event.target.value === "yes",
                        }))
                      }
                    >
                      <option value="no">No</option>
                      <option value="yes">Yes</option>
                    </select>
                  </label>
                </div>

                <label>
                  Image URL
                  <input
                    type="url"
                    value={productForm.image_url}
                    onChange={(event) =>
                      setProductForm((current) => ({ ...current, image_url: event.target.value }))
                    }
                  />
                </label>

                <label>
                  Materials (comma separated)
                  <input
                    type="text"
                    value={productForm.materials}
                    onChange={(event) =>
                      setProductForm((current) => ({ ...current, materials: event.target.value }))
                    }
                  />
                </label>

                <div className="admin-form-actions">
                  <button type="submit" className="primary-button">
                    {editingProductId ? "Save changes" : "Add product"}
                  </button>
                  {editingProductId ? (
                    <button type="button" className="secondary-button" onClick={resetProductForm}>
                      Cancel edit
                    </button>
                  ) : null}
                </div>
              </form>

              <form className="admin-card" onSubmit={onCreateCategory}>
                <h3>Add category</h3>
                <label>
                  Name
                  <input
                    type="text"
                    value={categoryForm.name}
                    onChange={(event) =>
                      setCategoryForm((current) => ({ ...current, name: event.target.value }))
                    }
                    required
                  />
                </label>
                <label>
                  Slug (optional)
                  <input
                    type="text"
                    value={categoryForm.slug}
                    onChange={(event) =>
                      setCategoryForm((current) => ({ ...current, slug: event.target.value }))
                    }
                    placeholder="auto from name if empty"
                  />
                </label>
                <label>
                  Description (optional)
                  <textarea
                    rows="2"
                    value={categoryForm.description}
                    onChange={(event) =>
                      setCategoryForm((current) => ({ ...current, description: event.target.value }))
                    }
                  />
                </label>
                <button type="submit" className="secondary-button">
                  Create category
                </button>
              </form>
            </section>

            <section className="admin-card" style={{ marginTop: "1rem" }}>
              <h3>Categories</h3>
              <div className="admin-table-wrap">
                <table className="admin-table">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Slug</th>
                      <th>Products</th>
                    </tr>
                  </thead>
                  <tbody>
                    {adminCategories.map((cat) => (
                      <tr key={cat.id}>
                        <td>{cat.name}</td>
                        <td className="muted">{cat.slug}</td>
                        <td>{cat.product_count ?? 0}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>

            <section className="admin-card admin-products-card" style={{ marginTop: "1rem" }}>
              <h3>Products</h3>
              <div className="admin-product-list">
                {products.length === 0 && <p className="muted">No products yet.</p>}

                {products.map((product) => (
                  <article key={product.id} className="admin-product-item">
                    <div>
                      <h4>{product.name}</h4>
                      <p className="muted">
                        {product.category_name} • ${Number(product.price).toFixed(2)} • Stock{" "}
                        {product.inventory_count}
                      </p>
                    </div>
                    <div className="admin-product-actions">
                      <button
                        type="button"
                        className="secondary-button"
                        onClick={() => onStartEditProduct(product)}
                      >
                        Edit
                      </button>
                      <button
                        type="button"
                        className="admin-delete-button"
                        onClick={() => onDeleteProduct(product.id)}
                      >
                        Delete
                      </button>
                    </div>
                  </article>
                ))}
              </div>
            </section>

            <section className="admin-card" style={{ marginTop: "1rem" }}>
              <h3>Orders</h3>
              <div className="admin-table-wrap">
                <table className="admin-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Customer</th>
                      <th>Total</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {orders.length === 0 && (
                      <tr>
                        <td colSpan={4} className="muted">
                          No orders yet.
                        </td>
                      </tr>
                    )}
                    {orders.map((order) => (
                      <tr key={order.id}>
                        <td>{order.id}</td>
                        <td>
                          {order.customer_name}
                          <br />
                          <span className="muted">{order.customer_email}</span>
                        </td>
                        <td>${Number(order.total).toFixed(2)}</td>
                        <td>
                          <select
                            value={order.status}
                            onChange={(event) => onOrderStatusChange(order.id, event.target.value)}
                            aria-label={`Status for order ${order.id}`}
                          >
                            {ORDER_STATUSES.map((s) => (
                              <option key={s} value={s}>
                                {s}
                              </option>
                            ))}
                          </select>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>

            <section className="admin-grid-2" style={{ marginTop: "1rem" }}>
              <div className="admin-card">
                <h3>Users</h3>
                <div className="admin-table-wrap">
                  <table className="admin-table">
                    <thead>
                      <tr>
                        <th>Name</th>
                        <th>Email</th>
                      </tr>
                    </thead>
                    <tbody>
                      {users.length === 0 && (
                        <tr>
                          <td colSpan={2} className="muted">
                            No registered users yet.
                          </td>
                        </tr>
                      )}
                      {users.map((u) => (
                        <tr key={u.id}>
                          <td>{u.name}</td>
                          <td className="muted">{u.email}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              <div className="admin-card">
                <h3>Contact messages</h3>
                <div className="admin-table-wrap">
                  <table className="admin-table">
                    <thead>
                      <tr>
                        <th>From</th>
                        <th>Message</th>
                      </tr>
                    </thead>
                    <tbody>
                      {messages.length === 0 && (
                        <tr>
                          <td colSpan={2} className="muted">
                            No messages yet.
                          </td>
                        </tr>
                      )}
                      {messages.map((msg) => (
                        <tr key={msg.id}>
                          <td>
                            {msg.name}
                            <br />
                            <span className="muted">{msg.email}</span>
                          </td>
                          <td>{msg.message}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </section>
          </>
        )}
      </div>
    </div>
  );
}

export default AdminPage;
