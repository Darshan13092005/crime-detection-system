# Installation Guide

## Prerequisites
- **Python** 3.10+
- **Node.js** 18+
- **Supabase Account** (For PostgreSQL & Auth)
- **Docker** (Optional, for containerized deployment)

---

## Local Development Setup

### 1. Database Setup
1. Create a new project in [Supabase](https://supabase.com/).
2. Run the SQL schema to create the `cameras`, `alerts`, `criminals`, and `events` tables.
3. Obtain your Project URL and Anon Key.

### 2. Backend (FastAPI & AI)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the `backend` folder based on `.env.example`:
```ini
SUPABASE_URL=your-project-url
SUPABASE_KEY=your-anon-key
SECRET_KEY=your-secret-key
TELEGRAM_BOT_TOKEN=...
```

Start the server:
```bash
uvicorn main:app --reload
```
*API will run on http://localhost:8000*

### 3. Frontend (React Dashboard)
```bash
cd frontend
npm install
```

Create a `.env` file in the `frontend` folder:
```ini
VITE_API_URL=http://localhost:8000/api/v1
```

Start the dashboard:
```bash
npm run dev
```
*Dashboard will run on http://localhost:5173*

---

## Docker Deployment
To deploy the entire stack using Docker Compose:

1. Create your `.env` file at the root.
2. Run:
```bash
docker-compose up -d --build
```
This builds both the Nginx container for the frontend and the Python container for the backend.
