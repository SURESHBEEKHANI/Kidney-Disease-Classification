import numpy as np
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing import image # type: ignore
import os

class PredictionPipeline:
    def __init__(self, filename):
        self.filename = filename

    def predict(self):
        # Define the path to the model
        model_path = os.path.join("model", "model.h5")
        
        # Check if the model file exists
        if not os.path.exists(model_path):
            raise FileNotFoundError("Model file not found at 'model/model.h5'")
        
        # Load model
        model = load_model(model_path)

        # Load and preprocess the image
        test_image = image.load_img(self.filename, target_size=(224, 224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)

        # Make prediction
        prediction_array = model.predict(test_image)
        result = np.argmax(prediction_array, axis=1)

        # Map the prediction to a label
        prediction = 'Tumor' if result[0] == 1 else 'Normal'
        
        # Return the result in a JSON-friendly format
        return {"prediction": prediction}
