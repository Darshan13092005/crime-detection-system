# Architecture

```mermaid
graph TD
    subaxis UI [Frontend - React/Vite]
    UI_Dash[Dashboard] --> UI_Stores[Zustand Stores]
    UI_Stores --> UI_API[Axios Client]
    end
    
    subaxis API [Backend - FastAPI]
    UI_API --> API_Router[FastAPI Router]
    API_Router --> API_Auth[Auth Service]
    API_Router --> API_AI[AI Stream Manager]
    API_Router --> API_DB[Supabase Client]
    end
    
    subaxis AI [AI Inference Pipeline]
    API_AI --> AI_Yolo[YOLOv8 Object/Pose]
    API_AI --> AI_Face[InsightFace Recognition]
    AI_Yolo --> AI_Events[Event Dispatcher]
    AI_Face --> AI_Events[Event Dispatcher]
    end
    
    subaxis DB [Supabase Cloud]
    API_DB --> DB_Pg[PostgreSQL]
    API_DB --> DB_Auth[GoTrue Auth]
    AI_Events --> DB_Pg
    end
    
    subaxis Notif [Notifications]
    AI_Events --> Notif_Telegram[Telegram Bot]
    AI_Events --> Notif_Email[SMTP Email]
    end
```
