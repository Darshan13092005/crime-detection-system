# Sentinel AI - Presentation Slides

> **Note**: Use these 12 slides to create your PowerPoint/Keynote presentation.

## Slide 1: Title Slide
- **Title**: Sentinel AI: Intelligent Crime Detection System
- **Subtitle**: Real-time Weapon, Violence, and Facial Recognition for Enterprise Security.
- **Presenter**: [Your Name/Team]
- **Date**: [Date]

## Slide 2: Problem Statement
- **The Issue**: Human operators suffer from fatigue when monitoring multiple CCTV feeds, leading to missed critical events.
- **The Risk**: Delayed response times to active shooters and violent altercations cost lives.
- **The Need**: An automated, tireless system that converts passive surveillance into active threat detection.

## Slide 3: Proposed Solution (Sentinel AI)
- **Concept**: A full-stack AI platform that integrates directly with existing RTSP/IP cameras.
- **Key Features**: Instant weapon detection, physical altercation tracking, and known-criminal facial recognition.
- **Outcome**: Millisecond-level threat detection alerting authorities via push notifications.

## Slide 4: System Architecture
- **Visual**: (Insert `architecture_diagram.md` graphic here)
- **Frontend**: React 19, Tailwind v4 (Control Room Dashboard).
- **Backend**: FastAPI (Python), asynchronous API handling.
- **Database**: Supabase (PostgreSQL + JWT Auth).

## Slide 5: The AI Inference Pipeline
- **Weapon & Violence Detection**: Powered by Ultralytics YOLOv8. Trained for high precision on edge devices.
- **Facial Recognition**: Utilizes InsightFace to match live frames against vector embeddings in our criminal database.
- **Optimization**: Multi-threaded camera streaming with frame-skipping logic to prevent CPU/GPU bottlenecks.

## Slide 6: Database & Data Flow
- **Visual**: (Insert `database_er_diagram.md` graphic here)
- **Storage**: Highly relational structure linking `Cameras` to `Alerts` to `Criminals`.
- **Evidence Management**: Snapshots of anomalies are instantly saved to S3 buckets for compliance and post-incident investigation.

## Slide 7: Real-Time Operator Dashboard
- **Visual**: (Insert Dashboard Screenshot)
- **Features**: Live metrics, active threat feeds, camera grid, and 24-hour incident charting via Recharts.
- **Design**: Dark-mode glassmorphism interface optimized for low-light control rooms.

## Slide 8: Security & Access Control
- **Role-Based Access**: Viewer, Operator, Commander, and Admin tiers.
- **Authentication**: JWT secured via Supabase GoTrue.
- **Audit Logging**: Custom FastAPI middleware logs every request IP and response time to monitor system health.

## Slide 9: Export & Compliance (Reports)
- **Functionality**: Law enforcement requires formal documentation.
- **Implementation**: Operators can export daily incident logs to PDF (jsPDF) and CSV (PapaParse) with a single click.

## Slide 10: Performance & Scalability
- **Deployment**: Fully containerized using Docker.
- **Edge vs Cloud**: Backend can be deployed on a local GPU node, while the React UI scales infinitely on PaaS (Vercel/Render).
- **Latency**: End-to-end detection to Telegram alert takes < 500ms on capable hardware.

## Slide 11: Future Scope
- **Multi-Camera Tracking**: Re-identification (Re-ID) of suspects across different camera zones.
- **Audio Analytics**: Integrating gunshot detection via audio streams.
- **Predictive Analytics**: Using historical data to predict high-risk zones.

## Slide 12: Conclusion & Q&A
- **Summary**: Sentinel AI proves that modern computer vision can be reliably packaged into a scalable, enterprise-ready web application to save lives.
- **Thank You!**
- **Questions?**
