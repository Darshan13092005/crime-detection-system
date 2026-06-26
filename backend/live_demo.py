import sys
import os
import cv2
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.ai.weapon_detection import WeaponDetector
from app.ai.fight_detection import FightDetector
from app.ai.face_recognition import FaceRecognitionModule
from app.ai.suspicious_activity import SuspiciousActivityDetector
from app.ai.event_dispatcher import EventDispatcher

def run_live_demo():
    print("--- Sentinel AI Live Demo ---")
    print("Initializing AI Models... (This might take a few seconds)")
    
    weapon_det = WeaponDetector()
    fight_det = FightDetector()
    face_rec = FaceRecognitionModule()
    suspicious_det = SuspiciousActivityDetector()
    dispatcher = EventDispatcher()
    
    print("✅ Models Initialized.")
    
    # Try opening webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error: Could not open webcam.")
        return

    print("🎥 Live feed started. Press 'q' in the video window to quit.")
    camera_id = "demo_cam_01"
    
    frame_count = 0
    skip_frames = 2 # Process every 2nd frame for smoother video if CPU bound

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            time.sleep(0.1)
            continue
            
        frame_count += 1
        
        # Only run heavy models every few frames
        if frame_count % skip_frames == 0:
            try:
                # The models modify the frame inplace by drawing boxes
                frame = face_rec.predict(frame, camera_id, dispatcher)
                frame = weapon_det.predict(frame, camera_id, dispatcher)
                frame = fight_det.predict(frame, camera_id, dispatcher)
                frame = suspicious_det.predict(frame, camera_id, dispatcher)
            except Exception as e:
                print(f"Inference error: {e}")

        # Add a helpful overlay
        cv2.putText(frame, "Sentinel AI Live", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow("Sentinel AI - Live Camera", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quitting live demo...")
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Demo terminated.")

if __name__ == "__main__":
    run_live_demo()
