from ultralytics import YOLO
import os

def train_model():
    # 1. Load the model
    model = YOLO("yolo11n.pt") 

    # 2. Path to your data.yaml
    # Verify this folder name matches exactly what is in your c:/dev/ folder
    dataset_path = os.path.join(os.getcwd(), "Construction-Site-Safety-1", "data.yaml")

    # 3. Start the Training
    model.train(
        data=dataset_path,
        epochs=50,
        imgsz=640,
        device="cuda",
        workers=0,          # SET TO 0: Stops the Windows multiprocessing crash
        batch=8,            # Lower batch size to keep your GPU from getting overwhelmed
        name="Safety_AI_v1",
        exist_ok=True,
        cache=False         # Helps if you have limited RAM
    )

if __name__ == '__main__':
    train_model()