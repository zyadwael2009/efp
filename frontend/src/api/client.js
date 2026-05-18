const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000/api";
const ADMIN_TOKEN_STORAGE_KEY = "efp_admin_token";

function cleanParams(params = {}) {
  return Object.fromEntries(
    Object.entries(params).filter(([, value]) => {
      if (value === undefined || value === null) {
        return false;
      }

      if (typeof value === "string") {
        return value.trim() !== "";
      }

      return true;
    })
  );
}

function buildQuery(params = {}) {
  const cleaned = cleanParams(params);
  const queryString = new URLSearchParams(cleaned).toString();
  return queryString ? `?${queryString}` : "";
}

function getStoredAdminToken() {
  try {
    return localStorage.getItem(ADMIN_TOKEN_STORAGE_KEY) || "";
  } catch (_error) {
    return "";
  }
}

function setStoredAdminToken(token) {
  try {
    if (token) {
      localStorage.setItem(ADMIN_TOKEN_STORAGE_KEY, token);
      return;
    }
    localStorage.removeItem(ADMIN_TOKEN_STORAGE_KEY);
  } catch (_error) {
    // Ignore localStorage errors in private browsing modes.
  }
}

async function apiRequest(path, options = {}) {
  const { headers: optionHeaders, ...rest } = options;
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...rest,
    headers: {
      "Content-Type": "application/json",
      ...(optionHeaders || {}),
    },
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.error || "Something went wrong while calling the API.");
  }

  return data;
}

export const api = {
  getHealth: () => apiRequest("/health"),

  getProducts: (params = {}) => apiRequest(`/products${buildQuery(params)}`),

  getProduct: (identifier) => apiRequest(`/products/${identifier}`),

  getCategories: () => apiRequest("/categories"),

  createOrder: (payload) =>
    apiRequest("/orders", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  createContactMessage: (payload) =>
    apiRequest("/users/contact", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  createOrUpdateUser: (payload) =>
    apiRequest("/users", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  getAdminToken: () => getStoredAdminToken(),

  clearAdminToken: () => setStoredAdminToken(""),

  adminLogin: async (payload) => {
    const data = await apiRequest("/admin/login", {
      method: "POST",
      body: JSON.stringify(payload),
    });

    if (data.token) {
      setStoredAdminToken(data.token);
    }

    return data;
  },

  getAdminProfile: (token = getStoredAdminToken()) =>
    apiRequest("/admin/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }),

  getAdminDashboard: (token = getStoredAdminToken()) =>
    apiRequest("/admin/dashboard", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }),

  getAdminProducts: (params = {}, token = getStoredAdminToken()) =>
    apiRequest(`/admin/products${buildQuery(params)}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }),

  createAdminProduct: (payload, token = getStoredAdminToken()) =>
    apiRequest("/admin/products", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    }),

  deleteAdminProduct: (productId, token = getStoredAdminToken()) =>
    apiRequest(`/admin/products/${productId}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }),

  patchAdminProduct: (productId, payload, token = getStoredAdminToken()) =>
    apiRequest(`/admin/products/${productId}`, {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    }),

  getAdminCategories: (token = getStoredAdminToken()) =>
    apiRequest("/admin/categories", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }),

  createAdminCategory: (payload, token = getStoredAdminToken()) =>
    apiRequest("/admin/categories", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    }),

  getAdminOrders: (params = {}, token = getStoredAdminToken()) =>
    apiRequest(`/admin/orders${buildQuery(params)}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }),

  updateAdminOrderStatus: (orderId, status, token = getStoredAdminToken()) =>
    apiRequest(`/admin/orders/${orderId}/status`, {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ status }),
    }),

  getAdminUsers: (params = {}, token = getStoredAdminToken()) =>
    apiRequest(`/admin/users${buildQuery(params)}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }),

  getAdminMessages: (params = {}, token = getStoredAdminToken()) =>
    apiRequest(`/admin/messages${buildQuery(params)}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }),
};
