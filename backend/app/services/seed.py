from ..extensions import db
from ..models import Admin, Category, Product, Review


PRODUCTS_DATA = [
    # ── CANDLES ─────────────────────────────────────────────────────────────
    {
        "name": "Bergamot & White Tea",
        "slug": "bergamot-white-tea",
        "short_description": "A clean, bright blend of bergamot citrus and delicate white tea.",
        "description": (
            "Hand-poured in small batches, our Bergamot & White Tea candle opens with sparkling bergamot "
            "and settles into a serene white tea heart. The coconut-soy base delivers a clean, even burn "
            "that fills the room without overwhelming. Perfect for a morning ritual or a quiet afternoon moment."
        ),
        "scent": "Citrus & Floral",
        "size": "8 oz",
        "burn_time": "45–55 hours",
        "price": 34.00,
        "featured": True,
        "inventory_count": 45,
        "materials": ["Coconut-Soy Blend", "Cotton Wick", "Recycled Glass Vessel"],
        "images": [
            "https://images.unsplash.com/photo-1602523961358-f9f03dd557bc?w=640&h=800&fit=crop&q=80"
        ],
        "category_slug": "candles",
        "reviews": [
            {
                "author": "Sophie M.",
                "title": "My everyday essential",
                "comment": "I've repurchased this three times now. The scent is subtle but long-lasting — fills my home office perfectly.",
                "rating": 5,
            },
            {
                "author": "James K.",
                "title": "Fresh and elegant",
                "comment": "Not too strong, not too light. Great throw and the glass vessel looks beautiful on my desk.",
                "rating": 5,
            },
            {
                "author": "Laura D.",
                "title": "Love the scent profile",
                "comment": "The bergamot is front and center but the white tea grounds it. Burns very evenly too.",
                "rating": 4,
            },
        ],
    },
    {
        "name": "Cedarwood & Amber",
        "slug": "cedarwood-amber",
        "short_description": "Warm, grounding cedarwood wrapped in a honey-sweet amber base.",
        "description": (
            "Cedarwood & Amber is our most-loved winter companion. A rich, woody opening of cedarwood transitions "
            "into a deep amber heart with subtle hints of vanilla musk. Ideal for creating a warm, cozy atmosphere "
            "on cooler evenings. The larger 12 oz pour ensures extended burn sessions."
        ),
        "scent": "Woody & Warm",
        "size": "12 oz",
        "burn_time": "65–75 hours",
        "price": 52.00,
        "featured": True,
        "inventory_count": 32,
        "materials": ["Pure Soy Wax", "Wooden Wick", "Matte Black Vessel"],
        "images": [
            "https://images.unsplash.com/photo-1581605405669-fcdf81165afa?w=640&h=800&fit=crop&q=80"
        ],
        "category_slug": "candles",
        "reviews": [
            {
                "author": "Rachel T.",
                "title": "The coziest scent",
                "comment": "I burn this every evening in the fall and winter. It makes my living room smell incredible.",
                "rating": 5,
            },
            {
                "author": "Michael B.",
                "title": "Bought as a gift, now I want one",
                "comment": "Gave this to my sister and now I'm ordering one for myself. The wooden wick crackle is a bonus.",
                "rating": 5,
            },
            {
                "author": "Nadia F.",
                "title": "Rich but not overpowering",
                "comment": "I was worried it would be too heavy but it's perfectly balanced. Great for a large room.",
                "rating": 4,
            },
        ],
    },
    {
        "name": "Lavender Dreams",
        "slug": "lavender-dreams",
        "short_description": "Classic French lavender softened with a touch of warm vanilla.",
        "description": (
            "A timeless scent, refined. Our Lavender Dreams candle uses premium French lavender essential oil "
            "layered over a light vanilla base that adds warmth without sweetness. Ideal for bedrooms, reading "
            "nooks, or any space where calm is a priority. The 6 oz size is perfectly portable for gifting or travel."
        ),
        "scent": "Floral & Herbal",
        "size": "6 oz",
        "burn_time": "30–40 hours",
        "price": 28.00,
        "featured": False,
        "inventory_count": 60,
        "materials": ["Coconut-Soy Blend", "Cotton Wick", "Frosted Glass Vessel"],
        "images": [
            "https://images.unsplash.com/photo-1467293622093-9f15c96be70f?w=640&h=800&fit=crop&q=80"
        ],
        "category_slug": "candles",
        "reviews": [
            {
                "author": "Anna W.",
                "title": "Best lavender candle I've tried",
                "comment": "I've tried many lavender candles and this is the most realistic — not synthetic-smelling at all.",
                "rating": 5,
            },
            {
                "author": "Carlos R.",
                "title": "Helps me sleep",
                "comment": "Light this an hour before bed and it completely transforms my bedroom routine.",
                "rating": 5,
            },
        ],
    },
    {
        "name": "Midnight Jasmine",
        "slug": "midnight-jasmine",
        "short_description": "Heady jasmine blossoms with a smoky, mysterious musk undertone.",
        "description": (
            "Midnight Jasmine is for those who prefer a more dramatic sensory experience. The top note of "
            "blooming jasmine unfolds into a complex musk base with whispers of dark amber and sandalwood. "
            "Burn after dusk for the full effect. This is our signature statement candle — bold, confident, and unforgettable."
        ),
        "scent": "Floral & Musk",
        "size": "10 oz",
        "burn_time": "55–65 hours",
        "price": 44.00,
        "featured": True,
        "inventory_count": 28,
        "materials": ["Pure Soy Wax", "Cotton Wick", "Smoked Glass Vessel"],
        "images": [
            "https://images.unsplash.com/photo-1612785289253-38a88e66ff83?w=640&h=800&fit=crop&q=80"
        ],
        "category_slug": "candles",
        "reviews": [
            {
                "author": "Elena V.",
                "title": "Absolutely stunning",
                "comment": "This is the most sophisticated candle I own. The scent is complex and evolves throughout the burn.",
                "rating": 5,
            },
            {
                "author": "Thomas H.",
                "title": "Great evening ambiance",
                "comment": "The smoked glass vessel paired with the jasmine scent creates perfect evening atmosphere.",
                "rating": 5,
            },
            {
                "author": "Priya S.",
                "title": "Unique and memorable",
                "comment": "I had guests asking what smelled so amazing. This is a conversation-starter candle.",
                "rating": 4,
            },
        ],
    },
    {
        "name": "Eucalyptus & Mint",
        "slug": "eucalyptus-mint",
        "short_description": "Invigorating eucalyptus with crisp spearmint — freshness defined.",
        "description": (
            "Eucalyptus & Mint is our go-to candle for energizing a space. The sharp, clean eucalyptus opens "
            "with a burst of green freshness, while spearmint adds a crisp, cool lift. Perfect for home offices, "
            "gyms, or bathrooms. Burns clean and leaves no waxy residue on the glass."
        ),
        "scent": "Fresh & Herbal",
        "size": "8 oz",
        "burn_time": "45–55 hours",
        "price": 34.00,
        "featured": False,
        "inventory_count": 50,
        "materials": ["Coconut-Soy Blend", "Cotton Wick", "Clear Glass Vessel"],
        "images": [
            "https://images.unsplash.com/photo-1574271143515-5cddf8da19be?w=640&h=800&fit=crop&q=80"
        ],
        "category_slug": "candles",
        "reviews": [
            {
                "author": "Jake L.",
                "title": "Perfect for my home office",
                "comment": "Burns while I work and keeps me focused. The scent is clean and doesn't distract.",
                "rating": 5,
            },
            {
                "author": "Mia C.",
                "title": "So refreshing",
                "comment": "Great in the bathroom. The eucalyptus makes the whole room feel like a spa.",
                "rating": 4,
            },
        ],
    },
    {
        "name": "Sandalwood Noir",
        "slug": "sandalwood-noir",
        "short_description": "Smooth Indian sandalwood deepened with dark patchouli and vanilla.",
        "description": (
            "Sandalwood Noir is our most indulgent formulation. Creamy Indian sandalwood forms the core, "
            "supported by rich patchouli and a base of warm vanilla and light musk. Long-lasting and sophisticated, "
            "this candle is designed for those who appreciate depth and complexity in their fragrance. The 12 oz "
            "pour makes it our best value for extended enjoyment."
        ),
        "scent": "Woody & Musky",
        "size": "12 oz",
        "burn_time": "65–75 hours",
        "price": 52.00,
        "featured": True,
        "inventory_count": 25,
        "materials": ["Pure Soy Wax", "Wooden Wick", "Matte White Vessel"],
        "images": [
            "https://images.unsplash.com/photo-1608181831718-c9fce3256cd1?w=640&h=800&fit=crop&q=80"
        ],
        "category_slug": "candles",
        "reviews": [
            {
                "author": "Isabelle N.",
                "title": "Luxury in a jar",
                "comment": "The creaminess of the sandalwood combined with the wooden wick crackle is just perfect.",
                "rating": 5,
            },
            {
                "author": "Andrei P.",
                "title": "Worth every penny",
                "comment": "I've bought premium candles at twice the price that didn't perform as well. Excellent quality.",
                "rating": 5,
            },
            {
                "author": "Grace T.",
                "title": "My signature scent now",
                "comment": "I burn this in my bedroom every night. My whole room smells amazing and it lasts forever.",
                "rating": 5,
            },
        ],
    },
    {
        "name": "Rose & Oud",
        "slug": "rose-oud",
        "short_description": "Velvety Damask rose layered over rare oud wood — pure luxury.",
        "description": (
            "Rose & Oud draws from Middle Eastern perfumery traditions to create a deeply luxurious experience. "
            "The full, velvety rose note opens beautifully before giving way to the warm, resinous depth of oud. "
            "This is a true prestige candle designed to fill larger spaces with an unmistakably sophisticated aroma."
        ),
        "scent": "Floral & Woody",
        "size": "8 oz",
        "burn_time": "45–55 hours",
        "price": 38.00,
        "featured": False,
        "inventory_count": 35,
        "materials": ["Coconut-Soy Blend", "Cotton Wick", "Rose Gold Vessel"],
        "images": [
            "https://images.unsplash.com/photo-1545450729-a69a0f8f95db?w=640&h=800&fit=crop&q=80"
        ],
        "category_slug": "candles",
        "reviews": [
            {
                "author": "Fatima A.",
                "title": "Absolutely beautiful",
                "comment": "The rose is so genuine and the oud gives it a depth that's hard to find in candles. Love it.",
                "rating": 5,
            },
            {
                "author": "Daniel M.",
                "title": "Bought for my wife, she loves it",
                "comment": "The rose gold vessel alone is stunning. The scent lives up to the presentation.",
                "rating": 4,
            },
        ],
    },
    {
        "name": "Coastal Breeze",
        "slug": "coastal-breeze",
        "short_description": "Sea salt air, driftwood, and a hint of fresh citrus peel.",
        "description": (
            "Coastal Breeze captures the feeling of an early morning walk along the shore. Sea salt opens "
            "fresh and airy, with driftwood adding an earthy calm and a whisper of citrus peel brightening "
            "the whole composition. Light and uplifting — the candle for sun-filled spaces, kitchens, and sun rooms."
        ),
        "scent": "Aquatic & Fresh",
        "size": "6 oz",
        "burn_time": "30–40 hours",
        "price": 28.00,
        "featured": False,
        "inventory_count": 55,
        "materials": ["Coconut-Soy Blend", "Cotton Wick", "Sea Glass Vessel"],
        "images": [
            "https://images.unsplash.com/photo-1620330867213-51c37b8dba59?w=640&h=800&fit=crop&q=80"
        ],
        "category_slug": "candles",
        "reviews": [
            {
                "author": "Olivia R.",
                "title": "Instant mood lift",
                "comment": "Light this on a grey day and suddenly it feels like summer. Truly a mood-enhancing candle.",
                "rating": 5,
            },
            {
                "author": "Ben F.",
                "title": "Great in the kitchen",
                "comment": "Keeps the kitchen smelling fresh and clean without competing with cooking smells.",
                "rating": 4,
            },
        ],
    },
    # ── HOME DECOR ───────────────────────────────────────────────────────────
    {
        "name": "Marble Display Tray",
        "slug": "marble-display-tray",
        "short_description": "Honed white marble tray — the perfect stage for your candles.",
        "description": (
            "Elevate your candle display with our honed white Carrara marble tray. Each piece is unique "
            "with natural grey veining. The smooth, matte surface protects your surfaces while providing "
            "a refined backdrop for your candle collection. Sized to hold two standard candles side by side. "
            "Hand-wash only."
        ),
        "scent": "N/A",
        "size": "30 × 15 cm",
        "burn_time": "N/A",
        "price": 48.00,
        "featured": False,
        "inventory_count": 20,
        "materials": ["Honed Carrara Marble"],
        "images": [
            "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=640&h=800&fit=crop&q=80"
        ],
        "category_slug": "home-decor",
        "reviews": [
            {
                "author": "Charlotte B.",
                "title": "Stunning quality",
                "comment": "The marble is beautiful and heavy — feels very premium. My candles look incredible on it.",
                "rating": 5,
            },
            {
                "author": "Sam D.",
                "title": "Great centrepiece",
                "comment": "Put two candles on this and suddenly my coffee table looks like a hotel lobby.",
                "rating": 5,
            },
        ],
    },
    {
        "name": "Ceramic Candle Holder",
        "slug": "ceramic-candle-holder",
        "short_description": "Minimalist glazed ceramic holder for tea lights and votives.",
        "description": (
            "Handcrafted in small batches by our ceramic studio partner, this glazed holder brings a soft, "
            "artisanal touch to any surface. The reactive glaze creates subtle tonal variations in the matte "
            "finish, meaning each piece is truly unique. Compatible with standard tea lights and most votive candles."
        ),
        "scent": "N/A",
        "size": "8 cm diameter",
        "burn_time": "N/A",
        "price": 32.00,
        "featured": False,
        "inventory_count": 30,
        "materials": ["Hand-Thrown Stoneware", "Reactive Glaze"],
        "images": [
            "https://images.unsplash.com/photo-1596524430615-b46475ddff6e?w=640&h=800&fit=crop&q=80"
        ],
        "category_slug": "home-decor",
        "reviews": [
            {
                "author": "Maria L.",
                "title": "Each one is unique",
                "comment": "The glaze variations are beautiful — mine has a subtle sage tone that wasn't in the photos.",
                "rating": 5,
            },
            {
                "author": "John R.",
                "title": "Perfect size",
                "comment": "Fits my tea lights perfectly and looks great on my windowsill.",
                "rating": 4,
            },
        ],
    },
    {
        "name": "Linen Candle Sleeve",
        "slug": "linen-candle-sleeve",
        "short_description": "Natural linen sleeve to dress your candle vessels elegantly.",
        "description": (
            "Transform any of our standard candle vessels with this natural linen sleeve. Handstitched with "
            "a delicate raw edge and a small brass button closure. The sleeve insulates the vessel, reducing "
            "surface heat while adding a tactile, organic layer to the aesthetic. One-size fits all 8 oz vessels."
        ),
        "scent": "N/A",
        "size": "One Size (8 oz fit)",
        "burn_time": "N/A",
        "price": 18.00,
        "featured": False,
        "inventory_count": 40,
        "materials": ["100% Natural Linen", "Brass Button"],
        "images": [
            "https://images.unsplash.com/photo-1615529151169-7b1ff50dc7f2?w=640&h=800&fit=crop&q=80"
        ],
        "category_slug": "home-decor",
        "reviews": [
            {
                "author": "Heather V.",
                "title": "Clever and pretty",
                "comment": "Didn't expect much from a sleeve but it genuinely transforms how the candle looks on a shelf.",
                "rating": 4,
            },
            {
                "author": "Lena K.",
                "title": "Great as gift wrapping",
                "comment": "Wrapped a candle in this as a gift and it looked so chic. Will buy more.",
                "rating": 5,
            },
        ],
    },
    {
        "name": "Terrazzo Coaster Set",
        "slug": "terrazzo-coaster-set",
        "short_description": "Set of four terrazzo coasters — protect and decorate in one.",
        "description": (
            "Our Terrazzo Coaster Set brings a playful yet refined touch to your candle ritual. Each coaster "
            "is hand-pressed with a unique mix of white terrazzo with rose and sage flecks, sealed with a "
            "food-safe resin for easy cleaning. Use them under our candle vessels or as standalone table accents. "
            "Set of 4."
        ),
        "scent": "N/A",
        "size": "10 cm each",
        "burn_time": "N/A",
        "price": 36.00,
        "featured": False,
        "inventory_count": 25,
        "materials": ["Terrazzo Composite", "Food-Safe Resin Seal"],
        "images": [
            "https://images.unsplash.com/photo-1550581190-9c1c48d21d6c?w=640&h=800&fit=crop&q=80"
        ],
        "category_slug": "home-decor",
        "reviews": [
            {
                "author": "Zoe M.",
                "title": "Lovely set",
                "comment": "Beautiful coasters that work perfectly under my candles. The terrazzo pattern is gorgeous.",
                "rating": 5,
            },
            {
                "author": "Patrick H.",
                "title": "Great quality",
                "comment": "Much sturdier than expected and the pattern is more beautiful in person than in photos.",
                "rating": 5,
            },
        ],
    },
    # ── FRAGRANCES ───────────────────────────────────────────────────────────
    {
        "name": "Bergamot Room Spray",
        "slug": "bergamot-room-spray",
        "short_description": "Instant room refresh with our signature Bergamot & White Tea scent.",
        "description": (
            "Our Bergamot Room Spray delivers the same beloved scent profile as our candle in an "
            "instant-gratification format. A few spritzes transform any room immediately. Formulated with "
            "an alcohol-free water base and fine fragrance oils, safe for upholstery, curtains, and linens. "
            "100 ml glass bottle with a reusable fine-mist pump."
        ),
        "scent": "Citrus & Floral",
        "size": "100 ml",
        "burn_time": "N/A",
        "price": 28.00,
        "featured": False,
        "inventory_count": 45,
        "materials": ["Fine Fragrance Oil", "Deionised Water", "Glass Bottle"],
        "images": [
            "https://images.unsplash.com/photo-1585386959984-a4155224a1ad?w=640&h=800&fit=crop&q=80"
        ],
        "category_slug": "fragrances",
        "reviews": [
            {
                "author": "Nina P.",
                "title": "My morning ritual",
                "comment": "I spray this in the bedroom before I leave for work. Coming home to that scent is a joy.",
                "rating": 5,
            },
            {
                "author": "Oscar L.",
                "title": "Smells exactly like the candle",
                "comment": "Great for rooms where I can't burn a candle. Perfect for hotel rooms when travelling.",
                "rating": 5,
            },
        ],
    },
    {
        "name": "Coastal Reed Diffuser",
        "slug": "coastal-reed-diffuser",
        "short_description": "Long-lasting continuous fragrance with our Coastal Breeze blend.",
        "description": (
            "Our Coastal Reed Diffuser provides effortless, long-lasting fragrance for up to 3 months. "
            "The premium Coastal Breeze oil blend is presented in a hand-blown amber glass bottle with 8 "
            "rattan reeds. Simply flip the reeds once a week for a fresh burst of sea salt and driftwood. "
            "Covers up to 40 sq m."
        ),
        "scent": "Aquatic & Fresh",
        "size": "200 ml",
        "burn_time": "Up to 3 months",
        "price": 56.00,
        "featured": False,
        "inventory_count": 20,
        "materials": ["Premium Fragrance Oil", "Amber Glass Vessel", "Rattan Reeds"],
        "images": [
            "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?w=640&h=800&fit=crop&q=80"
        ],
        "category_slug": "fragrances",
        "reviews": [
            {
                "author": "Emma R.",
                "title": "3 months and still going",
                "comment": "Already at the 2-month mark and it's still diffusing beautifully. Excellent longevity.",
                "rating": 5,
            },
            {
                "author": "Felix B.",
                "title": "Subtle but present",
                "comment": "Not overwhelming — just a constant gentle freshness. Exactly what I wanted for my hallway.",
                "rating": 4,
            },
        ],
    },
    {
        "name": "Aura Linen Mist",
        "slug": "aura-linen-mist",
        "short_description": "Delicate fabric spray — freshen your linens with Sandalwood Noir.",
        "description": (
            "Aura Linen Mist brings the depth of our Sandalwood Noir fragrance to your bedding, towels, "
            "and soft furnishings. The ultra-fine mist formula is designed not to mark or stain fabric, "
            "and the alcohol-free base is gentle on natural fibres. Two to three spritzes on a pillow at "
            "bedtime creates a calming, spa-like ritual. 150 ml amber glass bottle."
        ),
        "scent": "Woody & Musky",
        "size": "150 ml",
        "burn_time": "N/A",
        "price": 32.00,
        "featured": False,
        "inventory_count": 35,
        "materials": ["Fine Fragrance Oil", "Deionised Water", "Amber Glass Bottle"],
        "images": [
            "https://images.unsplash.com/photo-1615397349754-cfa2066a298e?w=640&h=800&fit=crop&q=80"
        ],
        "category_slug": "fragrances",
        "reviews": [
            {
                "author": "Chloe A.",
                "title": "Changed my bedtime routine",
                "comment": "I spray this on my pillow every night. The sandalwood is calming and lasts through the night.",
                "rating": 5,
            },
            {
                "author": "Pierre G.",
                "title": "Smells incredible on linens",
                "comment": "No staining, no overpowering — just a beautiful warm scent that lingers for days.",
                "rating": 5,
            },
        ],
    },
    # ── GIFTS ────────────────────────────────────────────────────────────────
    {
        "name": "The Ritual Set",
        "slug": "the-ritual-set",
        "short_description": "Our bestselling trio: one candle, one room spray, one marble tray.",
        "description": (
            "The Ritual Set is our most complete gifting experience. It includes one full-size 8 oz candle "
            "(scent of your choice), the matching 100 ml Room Spray, and a mini marble display tray — "
            "everything needed to establish a proper fragrance ritual. Presented in a rigid matte box with "
            "tissue paper and a hand-written notecard. Choose your preferred scent combination at checkout."
        ),
        "scent": "Choose at checkout",
        "size": "Gift Set",
        "burn_time": "Varies",
        "price": 89.00,
        "featured": True,
        "inventory_count": 15,
        "materials": ["Varies by selection", "Rigid Gift Box", "Tissue Paper"],
        "images": [
            "https://images.unsplash.com/photo-1549465220-1a8b9238cd48?w=640&h=800&fit=crop&q=80"
        ],
        "category_slug": "gifts",
        "reviews": [
            {
                "author": "Hannah W.",
                "title": "Perfect gift",
                "comment": "Bought this for my mother's birthday. The packaging alone made her emotional — so beautiful.",
                "rating": 5,
            },
            {
                "author": "Robert C.",
                "title": "The whole package",
                "comment": "I've never given a gift that was so well-received. The presentation is exceptional.",
                "rating": 5,
            },
            {
                "author": "Yuki S.",
                "title": "Worth the price",
                "comment": "Everything about this set is high quality. The marble tray alone is worth more than this.",
                "rating": 5,
            },
        ],
    },
    {
        "name": "The Minimalist Bundle",
        "slug": "the-minimalist-bundle",
        "short_description": "Two candles of your choice, paired and presented simply.",
        "description": (
            "The Minimalist Bundle is for those who know what they want: two candles, beautifully presented. "
            "Choose any two candles from our collection and we'll present them in a matte black two-slot box "
            "with a subtle embossed logo. Understated and elegant — this bundle lets the candles speak for themselves."
        ),
        "scent": "Choose at checkout",
        "size": "Bundle",
        "burn_time": "Varies",
        "price": 68.00,
        "featured": False,
        "inventory_count": 20,
        "materials": ["Varies by selection", "Matte Black Box"],
        "images": [
            "https://images.unsplash.com/photo-1607344645866-009c320b63e0?w=640&h=800&fit=crop&q=80"
        ],
        "category_slug": "gifts",
        "reviews": [
            {
                "author": "Claire F.",
                "title": "Elegant and simple",
                "comment": "Chose Bergamot & White Tea and Midnight Jasmine. The combination is perfect.",
                "rating": 5,
            },
            {
                "author": "Tom B.",
                "title": "Great housewarming gift",
                "comment": "This was a hit. Simple, classy, and the couple loved both scents.",
                "rating": 4,
            },
        ],
    },
    {
        "name": "Discovery Mini Set",
        "slug": "discovery-mini-set",
        "short_description": "Five mini candles — explore the full collection before committing.",
        "description": (
            "Not sure which scent to commit to? Our Discovery Mini Set includes five 2 oz travel-size candles "
            "covering all our core scent families: Citrus, Woody, Floral, Fresh, and Musky. Each burns for "
            "12–15 hours, giving you a thorough sampling experience. Presented in a wooden tray with individual "
            "linen bags. The perfect introduction to the EFP collection."
        ),
        "scent": "Mixed Scent Collection",
        "size": "5 × 2 oz",
        "burn_time": "12–15 hours each",
        "price": 45.00,
        "featured": False,
        "inventory_count": 30,
        "materials": ["Coconut-Soy Blend", "Cotton Wicks", "Mini Glass Vessels", "Wooden Tray"],
        "images": [
            "https://images.unsplash.com/photo-1608613309860-3bce2cf2a1be?w=640&h=800&fit=crop&q=80"
        ],
        "category_slug": "gifts",
        "reviews": [
            {
                "author": "Sarah M.",
                "title": "Best way to start",
                "comment": "I was completely new to luxury candles and this let me find my favourites before spending more. Brilliant concept.",
                "rating": 5,
            },
            {
                "author": "Luis V.",
                "title": "Great variety",
                "comment": "All five scents are distinct and high quality. I ended up falling in love with the Woody ones.",
                "rating": 4,
            },
            {
                "author": "Amelia J.",
                "title": "Adorable packaging",
                "comment": "The wooden tray and linen bags are so cute. I kept the packaging to display on my dresser.",
                "rating": 5,
            },
        ],
    },
]

CATEGORIES_DATA = [
    {
        "name": "Candles",
        "slug": "candles",
        "description": "Handmade candles designed for elegant everyday rituals.",
    },
    {
        "name": "Home Decor",
        "slug": "home-decor",
        "description": "Curated pieces to shape calm and intentional spaces.",
    },
    {
        "name": "Fragrances",
        "slug": "fragrances",
        "description": "Signature scent experiences beyond the candle flame.",
    },
    {
        "name": "Gifts",
        "slug": "gifts",
        "description": "Refined gifting collections for every meaningful moment.",
    },
]


def _seed_categories():
    for cat_data in CATEGORIES_DATA:
        if not Category.query.filter_by(slug=cat_data["slug"]).first():
            db.session.add(Category(**cat_data))
    db.session.commit()


def _seed_products():
    if Product.query.count() > 0:
        return

    for product_data in PRODUCTS_DATA:
        reviews_data = product_data.pop("reviews", [])
        category_slug = product_data.pop("category_slug")

        category = Category.query.filter_by(slug=category_slug).first()
        if not category:
            continue

        product = Product(category_id=category.id, **product_data)
        db.session.add(product)
        db.session.flush()

        for review_data in reviews_data:
            db.session.add(Review(product_id=product.id, **review_data))

    db.session.commit()


def seed_database():
    _seed_categories()
    _seed_products()
