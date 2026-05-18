function AboutPage() {
  return (
    <div className="page container section about-page">
      <section className="section-header">
        <p className="eyebrow">About EFP</p>
        <h1>Crafted By Hand, Guided By Intention</h1>
      </section>

      <section className="split-section">
        <article className="story-card fade-up">
          <h3>Our Beginning</h3>
          <p>
            EFP started with one goal: create candles that feel as beautiful as they smell.
            Each piece is hand-poured in small batches with clean wax blends, premium oils, and
            thoughtful vessel design.
          </p>
        </article>

        <article className="story-card fade-up">
          <h3>Our Standard</h3>
          <p>
            We combine minimalist aesthetics with scent craftsmanship to deliver products that elevate
            daily routines. Quality, consistency, and calm luxury define every collection.
          </p>
        </article>

        <article className="story-card fade-up">
          <h3>Our Vision</h3>
          <p>
            Candles are our foundation, not the limit. The brand and architecture are intentionally built
            to scale into home decor, fragrances, gifts, and curated lifestyle essentials.
          </p>
        </article>
      </section>

      <section className="timeline-block">
        <h2>Future Expansion Roadmap</h2>
        <div className="timeline-grid">
          <article>
            <span>Phase 1</span>
            <h4>Core Candle Collections</h4>
            <p>Seasonal launches, signature scents, and premium gift-ready packaging.</p>
          </article>
          <article>
            <span>Phase 2</span>
            <h4>Home Decor Capsules</h4>
            <p>Objects and accents designed to pair with fragrance rituals.</p>
          </article>
          <article>
            <span>Phase 3</span>
            <h4>Fragrance Ecosystem</h4>
            <p>Diffusers, room mists, and layered scent experiences for the entire home.</p>
          </article>
        </div>
      </section>
    </div>
  );
}

export default AboutPage;
