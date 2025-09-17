from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
import os
import pickle

# Use environment variable for base URL
CONNECTIVITY_API_URL = os.environ.get("CONNECTIVITY_API_URL", "http://127.0.0.1:8000")

app = FastAPI(title="3xample Connectivity Analyzer API", version="1.0")

# Allow CORS for frontend usage (if using GitHub Pages or any frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to your domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML model
MODEL_PATH = "rf_model.pkl"
try:
    with open(MODEL_PATH, "rb") as f:
        rf_model = pickle.load(f)
    print("ML model loaded successfully.")
except Exception as e:
    rf_model = None
    print(f"Failed to load ML model: {e}")

# ----------------- Example Endpoints ----------------- #

@app.get("/")
def root():
    return {"message": "Welcome to 3xample Connectivity Analyzer API!"}

@app.post("/predict")
def predict(data: dict):
    try:
        features = data.get("features")
        if not features or len(features) != 3:
            return JSONResponse(status_code=400, content={"error": "Expected 3 features for prediction"})
        pred = rf_model.predict([features])
        return {"prediction": pred.tolist()}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# You can add /ping, /dns, /traceroute, /speedtest endpoints here if needed
# For Render deployment, make sure you handle timeouts and async properly

# ----------------- Custom OpenAPI ----------------- #
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="3xample Connectivity Analyzer API",
        version="1.0",
        description=f"API endpoints for connectivity analysis. Deployed at `{CONNECTIVITY_API_URL}`",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
