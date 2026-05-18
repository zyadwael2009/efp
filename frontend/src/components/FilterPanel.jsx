const scentOptions = [
  "Cedarwood & Amber",
  "Jasmine & White Musk",
  "Cotton & Air",
  "Fig & Vetiver",
  "Cedar & Patchouli",
  "Bergamot & Neroli",
  "Sandalwood & Cashmere",
  "Rose & Tonka",
];

const sizeOptions = ["200g", "220g", "240g", "250g", "280g", "300g", "320g"];

function FilterPanel({ filters, categories, onChange, onReset }) {
  return (
    <aside className="filter-panel">
      <div className="filter-head">
        <h3>Filters</h3>
        <button type="button" onClick={onReset}>
          Reset
        </button>
      </div>

      <label>
        Search
        <input
          type="search"
          name="search"
          value={filters.search}
          onChange={onChange}
          placeholder="Search by name"
        />
      </label>

      <label>
        Category
        <select name="category" value={filters.category} onChange={onChange}>
          <option value="">All categories</option>
          {categories.map((category) => (
            <option key={category.id} value={category.slug}>
              {category.name}
            </option>
          ))}
        </select>
      </label>

      <label>
        Scent
        <select name="scent" value={filters.scent} onChange={onChange}>
          <option value="">All scents</option>
          {scentOptions.map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      </label>

      <label>
        Size
        <select name="size" value={filters.size} onChange={onChange}>
          <option value="">All sizes</option>
          {sizeOptions.map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      </label>

      <div className="filter-row">
        <label>
          Min Price
          <input
            type="number"
            min="0"
            name="min_price"
            value={filters.min_price}
            onChange={onChange}
            placeholder="0"
          />
        </label>

        <label>
          Max Price
          <input
            type="number"
            min="0"
            name="max_price"
            value={filters.max_price}
            onChange={onChange}
            placeholder="200"
          />
        </label>
      </div>

      <label>
        Sort
        <select name="sort" value={filters.sort} onChange={onChange}>
          <option value="featured">Featured</option>
          <option value="newest">Newest</option>
          <option value="price_asc">Price: Low to high</option>
          <option value="price_desc">Price: High to low</option>
        </select>
      </label>
    </aside>
  );
}

export default FilterPanel;
