from app.ai.weapon_detection import WeaponDetector
from app.ai.fight_detection import FightDetector
from app.ai.face_recognition import FaceRecognitionModule
from app.ai.suspicious_activity import SuspiciousActivityDetector
from app.ai.event_dispatcher import EventDispatcher

class AIService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AIService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        print("[AIService] Initializing AI Models Globally...")
        self.weapon_det = WeaponDetector()
        self.fight_det = FightDetector()
        self.face_rec = FaceRecognitionModule()
        self.suspicious_det = SuspiciousActivityDetector()
        self.dispatcher = EventDispatcher()
        print("[AIService] AI Models Initialized.")
        
        self._initialized = True

# Global instance (lazy initialization can be handled here or inside endpoint to not block startup if desired. Let's do it immediately when imported)
try:
    ai_service = AIService()
except Exception as e:
    print(f"Warning: Failed to load models on startup: {e}")
    ai_service = None
