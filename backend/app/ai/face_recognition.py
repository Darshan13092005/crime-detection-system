import cv2
import numpy as np
import json
from insightface.app import FaceAnalysis
from app.ai.base_model import BaseAIModel

class FaceRecognitionModule(BaseAIModel):
    def __init__(self, confidence_threshold=0.6):
        super().__init__()
        self.confidence_threshold = confidence_threshold
        print(f"[FaceRecognitionModule] Initialized on device: {self.device}")
        
        self.app = FaceAnalysis(name='buffalo_l', providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        self.app.prepare(ctx_id=0 if self.device == 'cuda' else -1, det_size=(640, 640))
        
        self.known_criminals = []
        self._load_criminal_database()

    def _load_criminal_database(self):
        print(f"[FaceRecognition] Loaded {len(self.known_criminals)} criminals from DB.")

    def load_model(self):
        pass # Prepared in __init__

    def _compare_faces(self, face_emb, known_emb):
        # Calculate cosine similarity
        dot = np.dot(face_emb, known_emb)
        norm = np.linalg.norm(face_emb) * np.linalg.norm(known_emb)
        similarity = dot / norm
        return similarity

    def predict(self, frame, camera_id: str, dispatcher):
        faces = self.app.get(frame)
        
        for face in faces:
            emb = face.normed_embedding
            bbox = face.bbox.astype(int)
            x1, y1, x2, y2 = bbox
            
            # Draw standard face box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
            
            # Compare with database
            best_match = None
            highest_sim = 0.0
            
            for criminal in self.known_criminals:
                sim = self._compare_faces(emb, criminal["encoding"])
                if sim > highest_sim:
                    highest_sim = sim
                    best_match = criminal
            
            if highest_sim > self.confidence_threshold and best_match:
                # It's a match!
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3) # Red box for criminal
                cv2.putText(frame, f"WANTED: {best_match['name']} ({highest_sim:.2f})", 
                            (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                
                bbox_json = json.dumps({"x1": int(x1), "y1": int(y1), "x2": int(x2), "y2": int(y2)})
                dispatcher.dispatch_alert(
                    camera_id=camera_id,
                    alert_type="criminal_spotted",
                    severity="high",
                    description=f"Criminal {best_match['name']} spotted with {highest_sim:.2f} confidence.",
                    frame=frame
                )
        return frame
