import numpy as np
from PIL import Image
from keras.models import load_model

model = load_model("recycle_model.h5")

CLASSES = [
    "plastic",
    "paper",
    "glass",
    "metal",
    "organic",
    "e-waste"
]

def preprocess_image(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224,224))

    img = np.array(img)/255.0
    img = np.expand_dims(img, axis=0)

    return img


def predict(image_path):

    image = preprocess_image(image_path)

    preds = model.predict(image)[0]

    idx = np.argmax(preds)
    confidence = float(preds[idx])

    return CLASSES[idx], confidence