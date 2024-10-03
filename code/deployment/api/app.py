# app.py
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from preprocess import preprocess_data
import xgboost as xgb
import pandas as pd

# Create an empty XGBoost model instance
model = xgb.XGBClassifier()

# Load the model from the file
model.load_model('xgb_model.xgb')

# Load the trained model
# with open("model.pkl", "rb") as f:
#     model = pickle.load(f)

# Define the FastAPI app
app = FastAPI()


# Define the input data schema
class FlightInput(BaseModel):
    # sepal_length: float
    # sepal_width: float
    # petal_length: float
    # petal_width: float
    month: object
    day_of_month: object
    day_of_week: object
    dep_time: int
    unique_carrier: object
    origin: object
    dest: object
    distance: int


# Define the prediction endpoint
@app.post("/predict")
def predict(input_data: FlightInput):
    data = [[
        input_data.month,
        input_data.day_of_month,
        input_data.day_of_week,
        input_data.dep_time,
        input_data.unique_carrier,
        input_data.origin,
        input_data.dest,
        input_data.distance
    ]]

    # to df
    data = pd.DataFrame(data, columns=['Month', 'DayofMonth', 'DayOfWeek', 'DepTime', 'UniqueCarrier', 'Origin', 'Dest', 'Distance'])

    data = preprocess_data(data, train=False)

    prediction = model.predict_proba(data)[:, 1]
    prediction = [1 if x > 0.4 else 0 for x in prediction]
    return {"prediction": int(prediction[0])}

