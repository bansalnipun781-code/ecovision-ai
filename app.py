import os
from flask import Flask, request, render_template
from tensorflow.lite.python.interpreter import Interpreter
import numpy as np
from PIL import Image

app = Flask(__name__)

# Load TFLite model
interpreter = Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

classes = {'e-waste': 0, 'glass': 1, 'metal': 2, 'organic': 3, 'paper': 4, 'plastic': 5}


def predict(img):
    # preprocess image
    img = img.resize((224, 224))
    img = np.array(img).astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)

    # set input tensor
    interpreter.set_tensor(input_details[0]['index'], img)

    # run inference
    interpreter.invoke()

    # get output
    pred = interpreter.get_tensor(output_details[0]['index'])[0]

    class_idx = np.argmax(pred)
    confidence = float(np.max(pred))

    return classes[class_idx], confidence


def get_recommendation(category):
    rec = {
        "plastic": "Recycle plastic",
        "paper": "Recycle paper",
        "glass": "Recycle glass",
        "metal": "Recycle metal",
        "organic": "Compost it",
        "e-waste": "Dispose at e-waste center"
    }
    return rec[category]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]

        filepath = os.path.join("static", "uploaded.jpg")
        file.save(filepath)

        img = Image.open(filepath)

        result, conf = predict(img)
        rec = get_recommendation(result)

        return render_template(
            "index.html",
            result=result,
            rec=rec,
            conf=conf
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)