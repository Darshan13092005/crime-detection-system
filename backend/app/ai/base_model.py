import torch

class BaseAIModel:
    def __init__(self):
        # Automatically select GPU if available, else fallback to CPU
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"[{self.__class__.__name__}] Initialized on device: {self.device}")

    def load_model(self):
        raise NotImplementedError("Subclasses must implement load_model")

    def predict(self, frame):
        raise NotImplementedError("Subclasses must implement predict")
