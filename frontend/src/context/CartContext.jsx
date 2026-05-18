import { createContext, useContext, useEffect, useMemo, useState } from "react";

const CartContext = createContext(null);
const STORAGE_KEY = "efp_cart";

function loadStoredCart() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (_error) {
    return [];
  }
}

export function CartProvider({ children }) {
  const [items, setItems] = useState(loadStoredCart);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
  }, [items]);

  const addItem = (product, quantity = 1) => {
    setItems((current) => {
      const existing = current.find((item) => item.id === product.id);

      if (existing) {
        return current.map((item) =>
          item.id === product.id
            ? {
                ...item,
                quantity: Math.max(1, Math.min(item.quantity + quantity, product.inventory_count || 99)),
              }
            : item
        );
      }

      return [
        ...current,
        {
          id: product.id,
          slug: product.slug,
          name: product.name,
          image: product.image || product.images?.[0],
          price: Number(product.price),
          quantity: Math.max(1, quantity),
          inventory_count: product.inventory_count || 99,
        },
      ];
    });
  };

  const updateQuantity = (productId, quantity) => {
    setItems((current) =>
      current
        .map((item) =>
          item.id === productId
            ? {
                ...item,
                quantity: Math.max(1, Math.min(quantity, item.inventory_count || 99)),
              }
            : item
        )
        .filter((item) => item.quantity > 0)
    );
  };

  const removeItem = (productId) => {
    setItems((current) => current.filter((item) => item.id !== productId));
  };

  const clearCart = () => setItems([]);

  const value = useMemo(() => {
    const totalItems = items.reduce((sum, item) => sum + item.quantity, 0);
    const subtotal = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

    return {
      items,
      addItem,
      updateQuantity,
      removeItem,
      clearCart,
      totalItems,
      subtotal,
    };
  }, [items]);

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}

export function useCart() {
  const context = useContext(CartContext);

  if (!context) {
    throw new Error("useCart must be used inside CartProvider");
  }

  return context;
}
