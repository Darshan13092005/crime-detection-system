import sys
import os
import cv2
import numpy as np

# Add backend to path so we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.ai.stream_manager import StreamManager

def verify_ai_models():
    print("--- Sentinel AI System Verification ---")
    
    # 1. Initialize StreamManager (this loads YOLO and InsightFace)
    print("\n[1] Initializing Stream Manager and loading models...")
    try:
        manager = StreamManager()
        print("✅ Models loaded successfully!")
    except Exception as e:
        print(f"❌ Failed to load AI models: {e}")
        return False
        
    # 2. Test inference with a synthetic frame (black image)
    print("\n[2] Testing inference pipeline with a synthetic frame...")
    try:
        dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        camera_id = "test_cam_01"
        
        print(" -> Running Face Recognition...")
        manager.face_rec.predict(dummy_frame, camera_id, manager.dispatcher)
        print(" -> Running Weapon Detection...")
        manager.weapon_det.predict(dummy_frame, camera_id, manager.dispatcher)
        print(" -> Running Fight Detection...")
        manager.fight_det.predict(dummy_frame, camera_id, manager.dispatcher)
        print(" -> Running Suspicious Activity Detection...")
        manager.suspicious_det.predict(dummy_frame, camera_id, manager.dispatcher)
        
        print("✅ Inference pipeline completed successfully without crashing!")
    except Exception as e:
        print(f"❌ Inference pipeline crashed: {e}")
        return False
        
    print("\n✅ All AI Verification Tests Passed!")
    return True

if __name__ == "__main__":
    success = verify_ai_models()
    if not success:
        sys.exit(1)
