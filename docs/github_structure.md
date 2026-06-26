# GitHub Repository Structure

```text
sentinel-ai/
│
├── backend/                      # FastAPI Python Backend
│   ├── app/                      
│   │   ├── api/                  # API Routers & Middlewares (Auth, Auditing)
│   │   ├── core/                 # Config, Security, and Supabase client
│   │   ├── models/               # Database SQLAlchemy Models (If used)
│   │   ├── schemas/              # Pydantic validation schemas
│   │   ├── services/             # Business Logic (DB operations)
│   │   └── ai/                   # AI Inference Logic
│   │       ├── stream_manager.py # ThreadPool video processing
│   │       ├── yolo_models.py    # Weapon & Fight detection
│   │       └── face_models.py    # InsightFace recognition
│   ├── tests/                    # Pytest automated test suite
│   ├── main.py                   # FastAPI Application Entrypoint
│   └── requirements.txt          # Python Dependencies
│
├── frontend/                     # React + Vite Frontend
│   ├── src/
│   │   ├── api/                  # Axios HTTP client configuration
│   │   ├── components/           # Reusable UI components (ErrorBoundary, Topbar)
│   │   ├── pages/                # Main views (Dashboard, Alerts, Reports)
│   │   ├── store/                # Zustand global state (authStore, alertStore)
│   │   └── App.tsx               # React Router configuration
│   ├── package.json              # NPM Dependencies
│   └── tailwind.config.ts        # Tailwind CSS v4 Configuration
│
├── docs/                         # Documentation
│   ├── installation_guide.md     # Setup instructions
│   ├── user_manual.md            # End-user operator guide
│   └── screenshots.md            # System UI snapshots
│
├── portfolio/                    # Project Presentation & Diagrams
│   ├── architecture_diagram.md   
│   ├── database_er_diagram.md
│   ├── deployment_diagram.md
│   ├── ieee_report.md
│   ├── presentation_slides.md
│   └── viva_questions.md
│
├── .github/workflows/            # CI/CD Pipelines
│   └── ci.yml                    # Automated tests and builds
│
├── docker-compose.yml            # Multi-container deployment orchestrator
└── README.md                     # Root project overview
```
