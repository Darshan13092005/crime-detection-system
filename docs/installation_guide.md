# Installation & Setup Guide

## 1. Prerequisites
- **Python**: Version 3.12 or higher.
- **Node.js**: Version 20 or higher.
- **Docker**: Optional, but recommended for production.
- **Supabase Account**: Required for Database and Authentication.

## 2. Supabase Configuration
1. Create a new project in [Supabase](https://supabase.com).
2. Note your `Project URL` and `API Key`.
3. In the SQL Editor, execute the schema found in `portfolio/api_docs.md` to create the `cameras`, `alerts`, `criminals`, and `events` tables.

## 3. Local Development Setup

### Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory:
```env
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
ENVIRONMENT=development
```

Start the API:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
```

Create a `.env` file in the `frontend/` directory:
```env
VITE_API_URL=http://localhost:8000/api/v1
```

Start the Dashboard:
```bash
npm run dev
```

## 4. Docker Deployment (Recommended)
Ensure Docker is installed and running.

```bash
docker-compose build
docker-compose up -d
```
The dashboard will be available at `http://localhost:5173` and the API at `http://localhost:8000`.
