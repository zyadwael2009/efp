import { useEffect, useState } from "react";

import { api } from "../api/client";
import FilterPanel from "../components/FilterPanel";
import ProductCard from "../components/ProductCard";
import QuickViewModal from "../components/QuickViewModal";
import { useCart } from "../context/CartContext";

const defaultFilters = {
  search: "",
  category: "",
  scent: "",
  size: "",
  min_price: "",
  max_price: "",
  sort: "featured",
};

function filtersAreDefault(filters) {
  return Object.entries(defaultFilters).every(([key, value]) => filters[key] === value);
}

function ShopPage() {
  const { addItem } = useCart();
  const [filters, setFilters] = useState(defaultFilters);
  const [categories, setCategories] = useState([]);
  const [products, setProducts] = useState([]);
  const [pagination, setPagination] = useState({ page: 1, pages: 1, total: 0, has_next: false, has_prev: false });
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [quickViewProduct, setQuickViewProduct] = useState(null);

  useEffect(() => {
    const loadCategories = async () => {
      try {
        const response = await api.getCategories();
        setCategories(response.items || []);
      } catch (_error) {
        setCategories([]);
      }
    };

    loadCategories();
  }, []);

  useEffect(() => {
    const loadProducts = async () => {
      setLoading(true);
      setError("");

      try {
        const response = await api.getProducts({ ...filters, page, per_page: 9 });
        setProducts(response.items || []);
        setPagination(response.pagination || {});
      } catch (requestError) {
        setError(requestError.message);
      } finally {
        setLoading(false);
      }
    };

    loadProducts();
  }, [filters, page]);

  const handleFilterChange = (event) => {
    const { name, value } = event.target;
    setPage(1);
    setFilters((current) => ({ ...current, [name]: value }));
  };

  const resetFilters = () => {
    setPage(1);
    setFilters(defaultFilters);
  };

  return (
    <div className="page container section">
      <div className="section-header">
        <p className="eyebrow">Shop</p>
        <h1>Crafted Candles</h1>
        <p className="muted">Filter by scent, size, and price to find your next favorite ritual.</p>
      </div>

      <div className="shop-layout">
        <FilterPanel
          filters={filters}
          categories={categories}
          onChange={handleFilterChange}
          onReset={resetFilters}
        />

        <div>
          <p className="muted">{pagination.total || 0} products</p>

          {loading && <p className="muted">Loading products...</p>}
          {error && <p className="error-text">{error}</p>}

          {!loading && !error && products.length === 0 && (
            <div className="empty-state">
              <h3>{filtersAreDefault(filters) ? "Catalog is empty" : "No matches found"}</h3>
              <p>
                {filtersAreDefault(filters)
                  ? "Products will appear here once they are published from the admin panel."
                  : "Try widening your filters to explore more products."}
              </p>
            </div>
          )}

          {!loading && !error && products.length > 0 && (
            <div className="product-grid">
              {products.map((product) => (
                <ProductCard
                  key={product.id}
                  product={product}
                  onQuickView={setQuickViewProduct}
                  onAddToCart={addItem}
                />
              ))}
            </div>
          )}

          <div className="pagination-controls">
            <button type="button" onClick={() => setPage((current) => current - 1)} disabled={!pagination.has_prev}>
              Previous
            </button>
            <span>
              Page {pagination.page || 1} of {pagination.pages || 1}
            </span>
            <button type="button" onClick={() => setPage((current) => current + 1)} disabled={!pagination.has_next}>
              Next
            </button>
          </div>
        </div>
      </div>

      <QuickViewModal
        product={quickViewProduct}
        onClose={() => setQuickViewProduct(null)}
        onAddToCart={(product) => {
          addItem(product);
          setQuickViewProduct(null);
        }}
      />
    </div>
  );
}

export default ShopPage;
