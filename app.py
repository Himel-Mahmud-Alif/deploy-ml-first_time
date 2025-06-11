from flask import Flask, render_template, request, url_for
import joblib
import os

# Initialize the Flask application
app = Flask(__name__)

# --- Load the Trained Model Pipeline ---
# The model is loaded once when the application starts.
# model_path = os.path.join('models', 'Pipeline.joblib')
# try:
#     pipeline = joblib.load(model_path)
#     print("Model pipeline loaded successfully.")
# except FileNotFoundError:
#     print(f"Error: Model file not found at {model_path}. Please run training_script.py first.")
#     pipeline = None
# except Exception as e:
#     print(f"An error occurred while loading the model: {e}")
#     pipeline = None

import joblib
model = joblib.load(r"")
# --- Define Routes ---

@app.route('/')
def home():
    """Renders the home page."""
    return render_template('index.html')

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Handles the prediction request from the form.
    Processes the input message and returns the prediction result.
    """
    if model is None:
        # If the model failed to load, show an error message.
        return render_template('result.html', prediction_text="Error: Model not loaded. Please check server logs.")

    if request.method == 'POST':
        # Get the message from the form
        message = request.form['message']

        # The input message must be in an iterable (like a list) for the pipeline
        data = [message]

        # Make a prediction
        prediction_code = model.predict(data)[0]
        prediction_text = 'Spam' if prediction_code == 1 else 'Not Spam'

        # Render the result page with the prediction outcome
        return render_template('result.html', message=message, prediction=prediction_text)

    # If not a POST request, redirect to the home page
    return render_template('index.html')

# --- Run the Application ---
if __name__ == '__main__':
    # Use threaded=False to ensure the model is loaded safely in one thread
    app.run(debug=True, threaded=False)