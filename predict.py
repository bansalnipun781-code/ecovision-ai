import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite

# -------------------------------
# Load TFLite Model
# -------------------------------
interpreter = tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Waste Classes
CLASSES = [
    "plastic",
    "paper",
    "glass",
    "metal",
    "organic",
    "e-waste"
]


# -------------------------------
# Image Preprocessing
# -------------------------------
def preprocess_image(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))

    img_array = np.array(img, dtype=np.float32)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    return img_array


# -------------------------------
# Prediction Function
# -------------------------------
def predict(image_path):

    image = preprocess_image(image_path)

    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]['index'])[0]

    predicted_index = np.argmax(output)
    confidence = float(output[predicted_index])

    predicted_class = CLASSES[predicted_index]

    return predicted_class, confidence