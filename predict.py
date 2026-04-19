import tensorflow as tf
import numpy as np
from PIL import Image

# Load trained model
model = tf.keras.models.load_model("recycle_model.h5")

# IMPORTANT: UPDATE THIS AFTER CHECKING train_data.class_indices
classes = {0: 'e-waste', 1: 'glass', 2: 'metal', 3: 'organic', 4: 'paper', 5: 'plastic'}


def predict_image(img_path):
    # Load and preprocess image
    img = Image.open(img_path).convert("RGB")
    img = img.resize((224, 224))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    # Predict
    pred = model.predict(img)[0]

    # 🔍 Debug: print probabilities
    print("\n--- Prediction Probabilities ---")
    for i, prob in enumerate(pred):
        print(f"{classes[i]} : {prob:.4f}")

    # Get predicted class
    class_idx = np.argmax(pred)
    predicted_class = classes[class_idx]

    return predicted_class


def get_recommendation(category):
    recommendations = {
        "plastic": "Recycle or reuse plastic items",
        "paper": "Send to paper recycling",
        "glass": "Recycle glass containers",
        "metal": "Sell or recycle metal",
        "organic": "Use for composting",
        "e-waste": "Dispose at certified e-waste center"
    }
    return recommendations.get(category, "No recommendation available")


# 🔹 MAIN EXECUTION
if __name__ == "__main__":
    img_path = input("Enter image path: ")

    result = predict_image(img_path)

    print("\n✅ Final Prediction:", result)
    print("♻️ Recommendation:", get_recommendation(result))





