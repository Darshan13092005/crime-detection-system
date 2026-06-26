import cv2
import time
import asyncio
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from app.services.ai_service import ai_service

router = APIRouter()

async def generate_frames(request: Request):
    # Only open camera when a request starts
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[Stream] Error: Could not open camera.")
        return

    print("[Stream] Camera opened for live feed.")
    camera_id = "demo_cam_01"
    frame_count = 0
    skip_frames = 2

    try:
        while True:
            if await request.is_disconnected():
                break

            await asyncio.sleep(0.01) # Yield to event loop

            ret, frame = cap.read()
            if not ret:
                await asyncio.sleep(0.1)
                continue
                
            frame_count += 1

            if ai_service is not None and frame_count % skip_frames == 0:
                try:
                    # Run AI models (modifies frame in-place)
                    frame = ai_service.face_rec.predict(frame, camera_id, ai_service.dispatcher)
                    frame = ai_service.weapon_det.predict(frame, camera_id, ai_service.dispatcher)
                    frame = ai_service.fight_det.predict(frame, camera_id, ai_service.dispatcher)
                    frame = ai_service.suspicious_det.predict(frame, camera_id, ai_service.dispatcher)
                except Exception as e:
                    print(f"[Stream] Inference error: {e}")

            # Draw a quick overlay
            cv2.putText(frame, "Sentinel AI App Live", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Encode frame
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
                
            frame_bytes = buffer.tobytes()

            # Yield frame for multipart response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                   
    except asyncio.CancelledError:
        # Fired when the client disconnects
        print("[Stream] Client disconnected.")
    finally:
        cap.release()
        print("[Stream] Camera released.")

@router.get("/live")
async def get_live_stream(request: Request):
    """
    Returns an MJPEG stream of the local camera (webcam).
    """
    return StreamingResponse(generate_frames(request), media_type="multipart/x-mixed-replace; boundary=frame")
