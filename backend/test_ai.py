import time
import os
from dotenv import load_dotenv

# Ensure we load env vars so supabase client doesn't crash if imported
load_dotenv(".env")

from app.ai.stream_manager import StreamManager

def run_test():
    print("=== Sentinel AI Modules Test ===")
    
    # Initialize the manager
    manager = StreamManager()
    
    # Camera 0 usually refers to the default webcam
    # We will use '0' to test the AI modules against the local webcam
    # Note: On a headless server, this will fail. You can replace '0' with a path to an MP4 video.
    manager.add_camera("test_cam_01", "0")
    
    print("Processing stream... press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
        manager.remove_camera("test_cam_01")
        print("Done.")

if __name__ == "__main__":
    run_test()
