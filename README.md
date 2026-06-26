# 🛡️ Sentinel AI - Intelligent Crime Detection System

![Sentinel AI Cover](assets/cover.png)

Sentinel AI is an enterprise-grade, real-time video surveillance and threat detection platform. It leverages advanced computer vision models to automatically detect weapons, physical violence, and known criminals, alerting authorities in real-time.

## ✨ Core Features
- **🔫 Weapon Detection**: Uses YOLOv8 to instantly identify firearms and bladed weapons.
- **🥊 Violence Detection**: Utilizes pose estimation to detect physical altercations.
- **👤 Facial Recognition**: Integrates with InsightFace to match live faces against a secure criminal database.
- **📊 Real-Time Dashboard**: A React + Vite + Tailwind v4 dark-themed interface for control room operators.
- **🔔 Automated Alerts**: Push notifications to Telegram and Email upon threat detection.

## 🛠️ Tech Stack
- **Frontend**: React 19, TypeScript, Vite, Tailwind CSS v4, Zustand, Recharts.
- **Backend**: Python 3.12+, FastAPI, PyTorch, Ultralytics YOLO, ONNXRuntime.
- **Database**: Supabase (PostgreSQL + GoTrue Auth).

## 🚀 Quick Start (Docker)
1. Clone the repository.
2. Provide your `.env` variables (see `.env.example`).
3. Run `docker-compose up --build -d`.
4. Access the dashboard at `http://localhost:5173`.

## 📚 Documentation
Please view the `/docs` and `/portfolio` directories for comprehensive documentation including:
- Installation & Deployment Guides
- User Manuals
- Academic Project Reports & Viva Questions
- System Architecture Diagrams

---
*Developed for production-ready intelligent surveillance.*
