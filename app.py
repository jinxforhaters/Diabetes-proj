#################################################################Flask####################################################
# # --- Import Core Libraries ---
# from flask import Flask, request, jsonify 
# import joblib
# import pandas as pd
# import numpy as np

# # --- Load the Trained Machine Learning Pipeline ---
# pipeline_path = 'diabetes_pipeline.joblib'
# loaded_pipeline = joblib.load(pipeline_path)
# print(f"Model pipeline from '{pipeline_path}' loaded successfully.")

# # --- Create the Flask App Instance ---
# app = Flask(__name__)

# from flask_cors import CORS
# CORS(app)
# # --- Define API Endpoints ---

# # This is the home/root route of our API
# @app.route('/', methods=['GET'])
# def home():
#     # This function is executed when someone navigates to the base URL (e.g., http://127.0.0.1:5000)
#     # It provides a simple welcome message and confirms the API is running.
#     return jsonify({
#         "message": "Welcome to the Diabetes Prediction API!",
#         "description": "This is a machine learning service to predict the likelihood of diabetes.",
#         "endpoints": {
#             "/predict": {
#                 "method": "POST",
#                 "description": "Send patient data in JSON format to get a prediction.",
#                 "example_payload": {
#                     "Pregnancies": 6,
#                     "Glucose": 148,
#                     "BloodPressure": 72,
#                     "SkinThickness": 35,
#                     "Insulin": 0,
#                     "BMI": 33.6,
#                     "DiabetesPedigreeFunction": 0.627,
#                     "Age": 50
#                 }
#             }
#         }
#     })

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         data = request.get_json()
#         if data is None:
#             return jsonify({"error": "No JSON data received"}), 400

#         input_df = pd.DataFrame([data])
        
#         prediction = loaded_pipeline.predict(input_df)
#         prediction_probabilities = loaded_pipeline.predict_proba(input_df)

#     except Exception as e:
#         return jsonify({"error": f"Error during prediction: {e}"}), 400

#     # Prepare the JSON Response
#     final_prediction_class = int(prediction[0])
#     probabilities = prediction_probabilities[0]
#     prediction_label = "Diabetic" if final_prediction_class == 1 else "Non-Diabetic"

#     response_data = {
#         "prediction_class": final_prediction_class,
#         "prediction_label": prediction_label,
#         "confidence_scores": {
#             "Non-Diabetic": float(probabilities[0]),
#             "Diabetic": float(probabilities[1])
#         }
#     }
    
#     print(f"Sending response: {response_data}")
#     return jsonify(response_data)

# # This is the standard Python entry point.
# # The code inside this 'if' block will only run when you execute the script directly
# # (e.g., 'python app.py' in the terminal). It will not run if the script is imported as a module.
# if __name__ == '__main__':
#     # app.run() starts the Flask development web server.
#     # debug=True enables debug mode, which provides helpful error messages and automatically
#     # reloads the server when you make changes to the code. This is great for development.
#     app.run(debug=True)


################################################################FastApi@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# --- Import Core Libraries ---
# --- Import Core Libraries ---
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware



# Load model
pipeline_path = "diabetes_pipeline.joblib"
loaded_pipeline = joblib.load(pipeline_path)
print(f"✅ Model pipeline loaded from '{pipeline_path}'")

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (or ["http://127.0.0.1:5500"] if using Live Server)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# --------- Data Model for POST Request ----------
class PatientData(BaseModel):
    Pregnancies: int
    Glucose: float
    BloodPressure: float
    SkinThickness: float
    Insulin: float
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int

@app.get("/health")
async def health():
    return {"status": "ok", "message": "service is up"}

# --------- API Endpoints ----------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the frontend"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
async def predict(data: PatientData):
    """Predict diabetes using the ML pipeline"""
    try:
        features = np.array([[
            data.Pregnancies,
            data.Glucose,
            data.BloodPressure,
            data.SkinThickness,
            data.Insulin,
            data.BMI,
            data.DiabetesPedigreeFunction,
            data.Age
        ]])

        prediction = int(loaded_pipeline.predict(features)[0])
        probabilities = loaded_pipeline.predict_proba(features)[0]

        response = {
            "prediction": prediction,
            "prediction_label": "Diabetic" if prediction == 1 else "Non_Diabetic",
            "confidence_scores": {
                "Non_Diabetic": float(probabilities[0]),
                "Diabetic": float(probabilities[1])
            }
        }

        return JSONResponse(response)

    except Exception as e:
        return {"error": str(e)}
