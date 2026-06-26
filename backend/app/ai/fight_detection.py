import cv2
import math
from ultralytics import YOLO
from app.ai.base_model import BaseAIModel

class FightDetector(BaseAIModel):
    def __init__(self, history_frames=15, movement_threshold=50):
        super().__init__()
        # We use a pose estimation model to track skeletal movement
        self.model = YOLO('yolov8n-pose.pt')
        self.model.to(self.device)
        
        self.history_frames = history_frames
        self.movement_threshold = movement_threshold
        # Dictionary to track recent wrist/ankle speeds per track_id
        self.history = {} 

    def load_model(self):
        pass

    def predict(self, frame, camera_id: str, dispatcher):
        # We need tracking enabled to follow individuals over time
        # persist=True handles tracking in the background
        results = self.model.track(source=frame, persist=True, verbose=False)
        
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            keypoints = results[0].keypoints.xy.cpu().numpy() # [N, 17, 2]
            
            for box, track_id, kpts in zip(boxes, track_ids, keypoints):
                # kpts shape is (17, 2)
                # Typically, indices 9, 10 are wrists, 15, 16 are ankles in COCO format
                if kpts is None or len(kpts) == 0:
                    continue
                    
                wrists = [kpts[9], kpts[10]]
                
                if track_id not in self.history:
                    self.history[track_id] = []
                    
                self.history[track_id].append(wrists)
                if len(self.history[track_id]) > self.history_frames:
                    self.history[track_id].pop(0)
                    
                # Calculate movement speed/erratic behavior if we have enough history
                if len(self.history[track_id]) == self.history_frames:
                    start_wrists = self.history[track_id][0]
                    end_wrists = self.history[track_id][-1]
                    
                    # Compute displacement
                    dist1 = math.hypot(end_wrists[0][0] - start_wrists[0][0], end_wrists[0][1] - start_wrists[0][1])
                    dist2 = math.hypot(end_wrists[1][0] - start_wrists[1][0], end_wrists[1][1] - start_wrists[1][1])
                    
                    max_movement = max(dist1, dist2)
                    
                    if max_movement > self.movement_threshold:
                        # Draw warning
                        x1, y1, x2, y2 = box
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 165, 255), 2)
                        cv2.putText(frame, "VIOLENT MOVEMENT", (int(x1), int(y1)-10), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
                                    
                        dispatcher.dispatch_alert(
                            camera_id=camera_id,
                            alert_type="violence",
                            severity="high",
                            description=f"Violent or rapid erratic movement detected. Displacement: {max_movement:.1f}",
                            frame=frame
                        )
                        # Clear history to avoid spamming alerts for the same event repeatedly
                        self.history[track_id].clear()
                        
        return frame
