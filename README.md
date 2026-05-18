# EFP E-Commerce Platform

A modern, premium, and scalable e-commerce starter for EFP, designed to grow into a wider lifestyle catalog (home decor, fragrances, gifts).

## Stack

- **Frontend:** React + Vite (deployable to Netlify or Vercel)
- **Backend API:** Flask + SQLAlchemy (deployable to PythonAnywhere or Render)
- **Database:** SQLite by default, PostgreSQL-ready via `DATABASE_URL`

## Project Structure

```
efp/
├─ backend/
│  ├─ app/
│  │  ├─ routes/
│  │  ├─ services/
│  │  ├─ __init__.py
│  │  ├─ config.py
│  │  ├─ extensions.py
│  │  └─ models.py
│  ├─ scripts/
│  │  ├─ create_admin.py
│  │  └─ clear_store_data.py
│  ├─ .env.example
│  ├─ requirements.txt
│  ├─ run.py
│  └─ wsgi.py          ← PythonAnywhere entry point
├─ frontend/
│  ├─ src/
│  │  ├─ api/
│  │  ├─ components/
│  │  ├─ context/
│  │  ├─ pages/
│  │  ├─ App.jsx
│  │  ├─ index.css
│  │  └─ main.jsx
│  ├─ .env.example
│  ├─ package.json
│  └─ vite.config.js
└─ README.md
```

## Core Features

- Minimalist premium storefront design (black/white + gray tones)
- Responsive layout for desktop and mobile
- Theme toggle (light/dark monochrome)
- Home, Shop, Product, About, Contact pages
- Product filtering by category, scent, size, and price
- Product quick view modal
- Cart system with quantity updates and checkout
- Order creation flow via Flask API
- API-backed products, orders, users
- Admin authentication (login + protected management endpoints)
- Admin panel for product creation and catalog management
- **18 seeded products** across 4 categories with 42 customer reviews
- Scalable category model for future expansion

---

## Local Development

### Backend

```bash
cd efp
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Mac/Linux
pip install -r backend/requirements.txt
copy backend\.env.example backend\.env
python backend/run.py
```

API runs at `http://127.0.0.1:5000/api`. The database is created and seeded automatically on first run.

Create the admin account:
```bash
python backend/scripts/create_admin.py --email your@email.com --password "YourPassword" --name "Your Name"
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Frontend runs at `http://localhost:5173`. Admin panel: `http://localhost:5173/admin`

---

## Deployment: PythonAnywhere (Backend)

### 1. Upload the code

```bash
# In a PythonAnywhere Bash console:
git clone https://github.com/YOUR_USERNAME/efp.git
cd efp/backend
pip install -r requirements.txt
```

### 2. Create your `.env` file

```bash
# In ~/efp/backend/.env
SECRET_KEY=your-long-random-secret-key-here
FRONTEND_URL=https://efpp.netlify.app
NETLIFY_URL=https://efpp.netlify.app
# Optional override if you want to list multiple origins:
# CORS_ORIGINS=https://efpp.netlify.app,https://another-site.netlify.app
FLASK_DEBUG=false
```

### 3. Configure the Web App

In the PythonAnywhere **Web** tab:

| Setting | Value |
|---|---|
| Source code | `/home/<username>/efp/backend` |
| Working directory | `/home/<username>/efp/backend` |
| WSGI configuration file | *(click the link and replace the content)* |

In the **WSGI configuration file** editor, replace everything with:

```python
import sys
sys.path.insert(0, '/home/<username>/efp/backend')

import os
os.environ.setdefault('SECRET_KEY', 'replace-with-your-secret')
os.environ.setdefault('FLASK_DEBUG', 'false')

from wsgi import application
```

Or, if you have a `.env` file, just use:

```python
import sys
sys.path.insert(0, '/home/<username>/efp/backend')
from wsgi import application
```

### 4. Create the admin account

```bash
# In PythonAnywhere Bash console:
cd ~/efp/backend
python scripts/create_admin.py --email your@email.com --password "YourPassword" --name "Your Name"
```

The database and all 18 products/42 reviews are seeded automatically on first request.

### 5. Reload the web app

Click **Reload** in the PythonAnywhere Web tab. Your API will be live at:
`https://<username>.pythonanywhere.com/api`

---

## Deployment: Frontend (Netlify / Vercel)

### Netlify

- Root directory: `frontend`
- Build command: `npm run build`
- Publish directory: `dist`
- Environment variable: `VITE_API_BASE_URL=https://<username>.pythonanywhere.com/api`

### Vercel

- Root directory: `frontend`
- Framework preset: Vite
- Environment variable: `VITE_API_BASE_URL=https://<username>.pythonanywhere.com/api`

---

## API Endpoints

### Public

| Method | Path | Description |
|---|---|---|
| GET | `/api/health` | Health check |
| GET | `/api/products` | List products (filterable) |
| GET | `/api/products/:id_or_slug` | Get product detail |
| GET | `/api/categories` | List categories |
| POST | `/api/orders` | Create order |
| POST | `/api/users` | Create/update user |
| POST | `/api/users/contact` | Submit contact message |

Product query params: `search`, `category`, `scent`, `size`, `min_price`, `max_price`, `featured`, `sort` (`featured`, `newest`, `price_asc`, `price_desc`), `page`, `per_page`

### Admin (require `Authorization: Bearer <token>`)

| Method | Path | Description |
|---|---|---|
| POST | `/api/admin/login` | Login, receive token |
| GET | `/api/admin/me` | Current admin profile |
| GET | `/api/admin/dashboard` | Counts dashboard |
| GET/POST | `/api/admin/categories` | List / create categories |
| GET/POST | `/api/admin/products` | List / create products |
| PUT/PATCH | `/api/admin/products/:id` | Update product |
| DELETE | `/api/admin/products/:id` | Delete product |
| GET | `/api/admin/orders` | List orders |
| PATCH | `/api/admin/orders/:id/status` | Update order status |
| GET | `/api/admin/users` | List users |
| GET | `/api/admin/messages` | List contact messages |
