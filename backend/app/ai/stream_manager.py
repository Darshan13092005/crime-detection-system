import cv2
import threading
import time
from app.ai.face_recognition import FaceRecognitionModule
from app.ai.weapon_detection import WeaponDetector
from app.ai.fight_detection import FightDetector
from app.ai.suspicious_activity import SuspiciousActivityDetector
from app.ai.event_dispatcher import EventDispatcher

class StreamManager:
    def __init__(self):
        self.streams = {} # {camera_id: {"url": str, "thread": Thread, "stop_flag": bool}}
        self.dispatcher = EventDispatcher()
        
        # Initialize AI Modules (loaded onto GPU if available)
        print("[StreamManager] Initializing AI Modules...")
        self.face_rec = FaceRecognitionModule()
        self.weapon_det = WeaponDetector()
        self.fight_det = FightDetector()
        self.suspicious_det = SuspiciousActivityDetector()
        print("[StreamManager] Modules initialized.")

    def add_camera(self, camera_id: str, stream_url: str):
        if camera_id in self.streams:
            print(f"Camera {camera_id} already exists.")
            return
            
        print(f"Adding camera {camera_id} with URL {stream_url}")
        stop_flag = [] # Using a list so it's mutable inside the thread
        
        thread = threading.Thread(
            target=self._process_stream,
            args=(camera_id, stream_url, stop_flag),
            daemon=True
        )
        self.streams[camera_id] = {
            "url": stream_url,
            "thread": thread,
            "stop_flag": stop_flag
        }
        thread.start()

    def remove_camera(self, camera_id: str):
        if camera_id in self.streams:
            print(f"Stopping stream for camera {camera_id}")
            self.streams[camera_id]["stop_flag"].append(True)
            self.streams[camera_id]["thread"].join(timeout=2)
            del self.streams[camera_id]

    def _process_stream(self, camera_id: str, stream_url: str, stop_flag: list):
        cap = cv2.VideoCapture(stream_url)
        if not cap.isOpened():
            print(f"Error opening video stream or file for camera {camera_id}: {stream_url}")
            return

        frame_count = 0
        while not stop_flag:
            ret, frame = cap.read()
            if not ret:
                time.sleep(0.1)
                continue

            frame_count += 1
            
            # We can do fast operations on every frame (like motion detection)
            # But heavy DL models run every Nth frame
            if frame_count % skip_frames != 0:
                continue

            # Run inference asynchronously or sequentially
            # In production, use ThreadPoolExecutor for concurrent module inference on the same frame.
            try:
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                    executor.submit(self.face_rec.predict, frame, camera_id, self.dispatcher)
                    executor.submit(self.weapon_det.predict, frame, camera_id, self.dispatcher)
                    executor.submit(self.fight_det.predict, frame, camera_id, self.dispatcher)
                    executor.submit(self.suspicious_det.predict, frame, camera_id, self.dispatcher)
            except Exception as e:
                print(f"[{camera_id}] Inference error: {e}")

            # Optional: Show locally if running on a machine with a display (for testing)
            # cv2.imshow(f"Camera {camera_id}", frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

        cap.release()
        print(f"Stream {camera_id} processing terminated.")
