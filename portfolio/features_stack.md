# Sentinel AI - Features & Tech Stack

## Features
- **Real-Time Video Analytics**: Process multiple RTSP/HTTP streams concurrently.
- **Weapon Detection**: YOLOv8-based model identifies firearms and knives.
- **Violence Detection**: Posture and skeletal analysis to identify physical altercations.
- **Facial Recognition**: InsightFace integration for identifying known suspects/criminals.
- **Automated Alerts**: Real-time push notifications via Telegram and Email.
- **Evidence Management**: Automatic snapshot capturing and secure DB logging.
- **Enterprise Dashboard**: Dark-themed, responsive React dashboard with charts and PDF exports.
- **Role-Based Access Control**: Secure JWT authentication and tiered permissions.

## Tech Stack
- **Frontend**: React 19, TypeScript, Vite, Tailwind CSS v4, Framer Motion, Zustand, Recharts.
- **Backend**: Python 3.12+, FastAPI, Uvicorn.
- **AI/ML**: PyTorch, Ultralytics YOLOv8, InsightFace, ONNXRuntime.
- **Database**: Supabase (PostgreSQL), GoTrue Auth.
- **DevOps**: Docker, GitHub Actions, Pytest.
