import cv2
import time
from ultralytics import YOLO
from app.ai.base_model import BaseAIModel

class SuspiciousActivityDetector(BaseAIModel):
    def __init__(self, loiter_time_threshold=60):
        super().__init__()
        self.model = YOLO('yolov8n.pt')
        self.model.to(self.device)
        self.loiter_threshold = loiter_time_threshold
        # Tracks {track_id: {"start_time": t, "last_pos": (x,y)}}
        self.track_history = {}

    def load_model(self):
        pass

    def predict(self, frame, camera_id: str, dispatcher):
        results = self.model.track(source=frame, classes=[0], persist=True, verbose=False) # class 0 is person
        
        current_time = time.time()
        
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            
            for box, track_id in zip(boxes, track_ids):
                x1, y1, x2, y2 = box
                cx = (x1 + x2) / 2
                cy = (y1 + y2) / 2
                
                if track_id not in self.track_history:
                    self.track_history[track_id] = {
                        "start_time": current_time,
                        "last_pos": (cx, cy),
                        "alerted": False
                    }
                else:
                    data = self.track_history[track_id]
                    # Update position
                    data["last_pos"] = (cx, cy)
                    time_present = current_time - data["start_time"]
                    
                    if time_present > self.loiter_threshold and not data["alerted"]:
                        # Loitering detected
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)
                        cv2.putText(frame, "LOITERING", (int(x1), int(y1)-10), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                        
                        dispatcher.dispatch_alert(
                            camera_id=camera_id,
                            alert_type="suspicious_activity",
                            severity="medium",
                            description=f"Person ID {track_id} has been loitering for {time_present:.0f}s.",
                            frame=frame
                        )
                        data["alerted"] = True
        return frame
