# IEEE Project Report: Sentinel AI - Real-Time Intelligent Crime Detection System

## Abstract
Traditional surveillance systems rely entirely on human monitoring, leading to a high rate of missed anomalies due to operator fatigue. This paper presents *Sentinel AI*, an automated, full-stack computer vision system designed to detect weapons, physical violence, and known criminals in real-time. Utilizing Ultralytics YOLOv8 for object and pose estimation, alongside InsightFace for facial recognition, the system processes multiple RTSP streams concurrently. A FastAPI backend serves the inference data via WebSockets to a React-based control room dashboard, providing instantaneous alerts and reducing response times for law enforcement.

## I. Introduction
The ubiquity of CCTV cameras has generated an overwhelming amount of video data. However, the manual analysis of these feeds is highly inefficient. Active shooter events and violent altercations require immediate intervention. Sentinel AI bridges this gap by deploying deep learning models directly onto camera streams, transforming passive recording devices into proactive alert mechanisms.

## II. System Architecture
The architecture is divided into three primary tiers:
1.  **AI Inference Node**: A Python environment running PyTorch. A `StreamManager` class uses `concurrent.futures.ThreadPoolExecutor` to evaluate incoming frames without blocking the event loop.
2.  **API & Database**: FastAPI provides secure, JWT-authenticated REST endpoints. Data is persisted in PostgreSQL (via Supabase), which handles relational mapping of `Cameras`, `Alerts`, and `Criminals`.
3.  **Client Dashboard**: A modern React application utilizing Tailwind CSS v4 and Zustand for state management, presenting data to operators intuitively.

## III. Methodology
### A. Weapon and Violence Detection
We utilized YOLOv8 (You Only Look Once) due to its optimal balance of speed and mean Average Precision (mAP). For weapon detection, the model isolates bounding boxes around firearms and bladed weapons. For violence detection, YOLOv8-Pose analyzes skeletal keypoints to detect aggressive postural anomalies (e.g., fighting, striking).

### B. Facial Recognition
InsightFace, utilizing ArcFace loss, extracts 512-dimensional feature vectors from detected faces. These vectors are compared against a pre-populated database of known suspects. Cosine similarity thresholds determine positive matches.

### C. Alert Dispatch
Upon exceeding confidence thresholds, the system generates an `Alert` record in the database, captures a base64 or S3-backed snapshot, and triggers external Webhooks (e.g., Telegram bots) to notify officers on patrol.

## IV. Results & Performance
The system was tested on a local environment simulating multiple 1080p feeds.
-   **Inference Speed**: On CPU (CPUExecutionProvider), frame-skipping was necessary to maintain real-time UI responsiveness. On GPU (CUDA), the system comfortably processed 4 concurrent streams at >30 FPS.
-   **Dashboard Latency**: React state updates (via Zustand and Axios polling) reflected backend alerts in under 500ms.
-   **Security**: The implementation of `AuditMiddleware` and Role-Based Access Control (RBAC) ensures the system meets enterprise security compliance.

## V. Conclusion
Sentinel AI successfully demonstrates that integrating state-of-the-art computer vision models with modern web frameworks yields a highly effective security solution. Future iterations will focus on edge-deployment via TensorRT and multi-camera suspect tracking (Re-ID).

## References
[1] Redmon, J., et al. "You Only Look Once: Unified, Real-Time Object Detection." *CVPR*, 2016.
[2] Jocher, G., et al. "Ultralytics YOLOv8." *GitHub*, 2023.
[3] Deng, J., et al. "ArcFace: Additive Angular Margin Loss for Deep Face Recognition." *CVPR*, 2019.
