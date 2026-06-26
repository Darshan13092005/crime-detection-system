import cv2
import json
from ultralytics import YOLO
from app.ai.base_model import BaseAIModel

class WeaponDetector(BaseAIModel):
    def __init__(self, confidence_threshold=0.5):
        super().__init__()
        self.confidence_threshold = confidence_threshold
        # We use a standard YOLOv8 model for demonstration.
        # In a real scenario, this would be a fine-tuned model (e.g., 'yolov8n_weapons.pt')
        self.model = YOLO('yolov8n.pt') 
        self.model.to(self.device)
        
        # Suppose class IDs for weapons in our custom model are:
        # 0: handgun, 1: knife, 2: rifle (These are mock IDs for this example)
        # Standard COCO doesn't have handgun/rifle prominently isolated like this, 
        # but we pretend it's a fine-tuned model.
        self.weapon_classes = [0, 1, 2] 

    def load_model(self):
        # Model is loaded in __init__ for ultralytics
        pass

    def predict(self, frame, camera_id: str, dispatcher):
        """
        Runs YOLOv8 detection. If a weapon is detected above threshold, 
        dispatches an alert.
        """
        results = self.model.predict(source=frame, conf=self.confidence_threshold, verbose=False)
        detected_weapons = []
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls_id = int(box.cls[0].item())
                conf = float(box.conf[0].item())
                
                # Check if it's a weapon class
                if cls_id in self.weapon_classes:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    bbox = json.dumps({"x1": x1, "y1": y1, "x2": x2, "y2": y2})
                    detected_weapons.append((cls_id, conf, bbox))
                    
                    # Draw on frame for the snapshot
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                    cv2.putText(frame, f"Weapon: {conf:.2f}", (int(x1), int(y1)-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        if len(detected_weapons) > 0:
            # Dispatch highest confidence weapon alert
            best_det = max(detected_weapons, key=lambda x: x[1])
            dispatcher.dispatch_alert(
                camera_id=camera_id,
                alert_type="weapon_detected",
                severity="critical",
                description=f"Weapon detected with {best_det[1]:.2f} confidence.",
                frame=frame
            )
            
        return frame
