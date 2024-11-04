from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import os

# Import necessary modules for decoding images and prediction pipeline
from cnnClassifier.utils.common import decodeImage
from cnnClassifier.pipeline.prediction import PredictionPipeline

# Set environment variables for consistent locale settings
os.environ['LANG'] = 'en_US.UTF-8'
os.environ['LC_ALL'] = 'en_US.UTF-8'

# Initialize Flask app and allow cross-origin requests
app = Flask(__name__)
CORS(app)

class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        self.classifier = PredictionPipeline(self.filename)

# Instantiate the ClientApp globally to reuse the model
clApp = ClientApp()

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')

@app.route("/train", methods=['GET', 'POST'])
@cross_origin()
def trainRoute():
    os.system("python main.py")
    # Uncomment the following line if using DVC for model versioning
    # os.system("dvc repro")
    return "Training done successfully!"

@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRoute():
    try:
        # Ensure image data is present in the request
        if 'image' not in request.json:
            return jsonify({"error": "No image data provided"}), 400

        # Decode and save the incoming image
        image_data = request.json['image']
        decodeImage(image_data, clApp.filename)

        # Perform the prediction
        result = clApp.classifier.predict()
        return jsonify(result)

    except FileNotFoundError as e:
        # Handle model file not found error
        return jsonify({"error": f"Model file not found: {str(e)}"}), 500

    except Exception as e:
        # Handle any other errors
        return jsonify({"error": f"An error occurred during prediction: {str(e)}"}), 500

# Run the app in debug mode for development and troubleshooting
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
