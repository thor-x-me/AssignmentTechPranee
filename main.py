import io
import joblib
import pandas as pd
from pydantic import BaseModel
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from fastapi import FastAPI, File, UploadFile, HTTPException

app = FastAPI(title="Manufacturing Predictor API")
model = None
scaler = None

@app.post("/upload")
async def upload_data(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        data = pd.read_csv(io.StringIO(contents.decode('utf-8')))

        # Save the uploaded data
        joblib.dump(data, 'uploaded_data.joblib')
        return {"message": "Data uploaded successfully", "rows": len(data)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/train")
async def train_model():
    try:
        # Load the data
        data = joblib.load('uploaded_data.joblib')

        # Separate features and target
        X = data.drop('DefectStatus', axis=1)
        y = data['DefectStatus']

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Scale the features
        global scaler
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Train the model
        global model
        model = DecisionTreeClassifier(random_state=42)
        model.fit(X_train_scaled, y_train)

        # Calculate metrics
        y_pred = model.predict(X_test_scaled)
        metrics = {
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "f1_score": float(f1_score(y_test, y_pred, average='weighted'))
        }

        # Save the model and scaler
        joblib.dump(model, 'model.joblib')
        joblib.dump(scaler, 'scaler.joblib')

        return metrics

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class PredictionInput(BaseModel):
    ProductionVolume: float
    ProductionCost: float
    SupplierQuality: float
    DeliveryDelay: float
    DefectRate: float
    QualityScore: float
    MaintenanceHours: float
    DowntimePercentage: float
    InventoryTurnover: float
    StockoutRate: float
    WorkerProductivity: float
    SafetyIncidents: float
    EnergyConsumption: float
    EnergyEfficiency: float
    AdditiveProcessTime: float
    AdditiveMaterialCost: float


@app.post("/predict")
async def predict(input_data: PredictionInput):
    print("Received input data:", dict(input_data))
    try:

        # Load model and scaler if not in memory
        global model, scaler
        if model is None:
            model = joblib.load('model.joblib')
            scaler = joblib.load('scaler.joblib')

        # Prepare input data
        input_df = pd.DataFrame([{
            'ProductionVolume': input_data.ProductionVolume,
            'ProductionCost': input_data.ProductionCost,
            'SupplierQuality': input_data.SupplierQuality,
            'DeliveryDelay': input_data.DeliveryDelay,
            'DefectRate': input_data.DefectRate,
            'QualityScore': input_data.QualityScore,
            'MaintenanceHours': input_data.MaintenanceHours,
            'DowntimePercentage': input_data.DowntimePercentage,
            'InventoryTurnover': input_data.InventoryTurnover,
            'StockoutRate': input_data.StockoutRate,
            'WorkerProductivity': input_data.WorkerProductivity,
            'SafetyIncidents': input_data.SafetyIncidents,
            'EnergyConsumption': input_data.EnergyConsumption,
            'EnergyEfficiency': input_data.EnergyEfficiency,
            'AdditiveProcessTime': input_data.AdditiveProcessTime,
            'AdditiveMaterialCost': input_data.AdditiveMaterialCost
        }])

        # Scale input
        input_scaled = scaler.transform(input_df)

        # Make prediction
        prediction = model.predict(input_scaled)[0]
        confidence = float(max(model.predict_proba(input_scaled)[0]))

        return {
            "DefectStatus": "Yes" if prediction == 1 else "No",
            "Confidence": confidence
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
