# Sentinel AI - Viva / Defense Questions & Answers

## Artificial Intelligence & Computer Vision

**Q1: Why did you choose YOLOv8 over Faster R-CNN?**
*A:* YOLOv8 is a single-stage detector, making it significantly faster for real-time video processing than two-stage detectors like Faster R-CNN. For a security system where milliseconds matter, YOLO provides the best trade-off between mAP (accuracy) and inference speed (FPS).

**Q2: How does the fight detection work?**
*A:* Instead of just classifying image frames, we use YOLOv8-Pose to map the skeletal keypoints of individuals in the frame. We analyze the proximity and rapid movement vectors of these keypoints (e.g., overlapping bounding boxes with high velocity arm movements) over a sequence of frames to infer physical violence.

**Q3: What is InsightFace, and how does it compare to standard OpenCV face detection?**
*A:* OpenCV's Haar Cascades only *detect* faces. InsightFace is a deep learning framework (often using ArcFace) that *recognizes* faces. It extracts a 512-dimensional vector embedding of a face. We calculate the cosine similarity between the live camera face vector and our database vectors to find a match.

**Q4: How did you handle the performance bottleneck of running AI on every video frame?**
*A:* We implemented a frame-skipping algorithm in `stream_manager.py`. Since video runs at 30 FPS, running deep learning models on every single frame is redundant and CPU-intensive. We process every 3rd or 5th frame, maintaining high detection rates while drastically reducing hardware load.

## Backend Architecture (FastAPI & Python)

**Q5: Why FastAPI instead of Django or Flask?**
*A:* FastAPI is built on Starlette and Pydantic, making it natively asynchronous and extremely fast. Since we are handling continuous video streams and concurrent alert webhooks, the non-blocking async nature of FastAPI is vastly superior to Flask for this use case.

**Q6: Explain your ThreadPool implementation in the Stream Manager.**
*A:* Python's Global Interpreter Lock (GIL) can block execution. By using `concurrent.futures.ThreadPoolExecutor`, we allow the different AI modules (Face, Weapon, Fight) to process the same video frame concurrently on different threads, rather than waiting for one model to finish before starting the next.

**Q7: How did you implement security and API protection?**
*A:* We implemented JWT (JSON Web Token) authentication. We also built a custom FastAPI dependency `require_role` which checks the user's role (Admin, Operator) in the token before allowing them to hit endpoints. Finally, we added an `AuditMiddleware` to log every incoming IP address and request duration.

## Frontend (React) & Database (Supabase)

**Q8: Why use Zustand instead of Redux for state management?**
*A:* Zustand is a minimalist, unopinionated state manager that requires far less boilerplate than Redux. For handling our `alertStore` and `cameraStore` real-time states, Zustand provided a much cleaner and faster development experience.

**Q9: How are the PDF and CSV reports generated entirely on the frontend?**
*A:* We utilize `jsPDF` for drawing the PDF layout programmatically using canvas, and `PapaParse` to convert JSON array data into raw CSV blobs. The browser then triggers a local download, which saves backend server bandwidth.

**Q10: Why did you choose PostgreSQL (Supabase) over MongoDB?**
*A:* A crime detection system is highly relational. An Alert belongs to a Camera, and may be linked to a specific Criminal. PostgreSQL's relational integrity (Foreign Keys) prevents orphaned data. Additionally, Supabase provides built-in Row Level Security (RLS) and GoTrue authentication right out of the box.
