# Sentinel AI - Deployment Guide

This guide details how to deploy the full Sentinel AI architecture for production.

## Docker Deployment (VPS / Self-Hosted)

For maximum performance (especially for AI inference), running a dedicated VPS with an NVIDIA GPU is highly recommended.

1. **Prerequisites**: Docker, Docker Compose, and NVIDIA Container Toolkit.
2. **Environment**: Create a `.env` file in the root containing your real `SUPABASE_URL` and `SUPABASE_KEY`.
3. **Run**:
   ```bash
   docker-compose build
   docker-compose up -d
   ```

## Cloud PaaS (Render / Railway)

If you are only running the API and Dashboard (and offloading AI inference elsewhere), you can deploy via PaaS.

### Backend (Render)
1. Connect your GitHub repository to Render.
2. Create a new **Web Service**.
3. **Build Command**: `pip install -r backend/requirements.txt`
4. **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. **Environment Variables**: Add `SUPABASE_URL`, `SUPABASE_KEY`, `ENVIRONMENT=production`.

### Frontend (Vercel / Netlify / Railway)
1. Set the root directory to `frontend`.
2. **Build Command**: `npm run build`
3. **Output Directory**: `dist`
4. **Environment Variables**: `VITE_API_URL=https://your-render-app.onrender.com/api/v1`

## Continuous Integration (GitHub Actions)
The project includes a `.github/workflows/ci.yml` that automatically lints and runs `pytest` on every push to `main`.
