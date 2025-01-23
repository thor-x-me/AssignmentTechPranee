# Manufacturing Predictor API - README

## Overview
The **Manufacturing Predictor API** is a FastAPI-based application that allows users to:
1. Upload manufacturing data for training a machine learning model.
2. Train a Decision Tree Classifier to predict the defect status of manufactured products.
3. Use the trained model to predict defect statuses based on input parameters.

This API is designed to assist in improving manufacturing processes by identifying potential defects based on various operational parameters.

---

## Features
- **Upload Data**: Upload the provided CSV file in the repository containing manufacturing data with a `DefectStatus` column (target variable).
- **Train Model**: Train a machine learning model using the uploaded data.
- **Predict**: Make predictions on whether a manufactured product is defective or not based on input features.

---

## Endpoints

### 1. **Upload Data**
**Endpoint**: `POST /upload`  
**Description**:  Upload the provided CSV file in the repository containing training data.  
**Request**:
- File upload (`file`): The CSV file.  
**Response**:
- JSON response indicating success and the number of rows in the uploaded data.

**Example Response**:
```json
{
  "message": "Data uploaded successfully",
  "rows": 100
}
```

---

### 2. **Train Model**
**Endpoint**: `POST /train`  
**Description**: Trains a Decision Tree Classifier on the uploaded data.  
**Request**: No input is required.  
**Response**:
- Metrics of the trained model (`accuracy` and `f1_score`).

**Example Response**:
```json
{
  "accuracy": 0.92,
  "f1_score": 0.91
}
```

---

### 3. **Predict**
**Endpoint**: `POST /predict`  
**Description**: Predicts the defect status of a manufactured product based on input features.  
**Request**:
- JSON body containing manufacturing parameters:
    - `ProductionVolume`, `ProductionCost`, `SupplierQuality`, etc. (16 input fields).

**Example Request**:
```json
{
  "ProductionVolume": 120.5,
  "ProductionCost": 45.3,
  "SupplierQuality": 8.0,
  "DeliveryDelay": 3.0,
  "DefectRate": 2.5,
  "QualityScore": 90.0,
  "MaintenanceHours": 10.0,
  "DowntimePercentage": 4.5,
  "InventoryTurnover": 15.0,
  "StockoutRate": 2.0,
  "WorkerProductivity": 75.0,
  "SafetyIncidents": 1.0,
  "EnergyConsumption": 500.0,
  "EnergyEfficiency": 85.0,
  "AdditiveProcessTime": 20.0,
  "AdditiveMaterialCost": 30.0
}
```

**Response**:
- Predicted defect status (`Yes`/`No`) and the confidence score.

**Example Response**:
```json
{
  "DefectStatus": "No",
  "Confidence": 0.87
}
```

---

## Data Requirements
1. The uploaded CSV file must contain the following:
   - **Features**: Operational parameters (e.g., `ProductionVolume`, `EnergyConsumption`, etc.).
   - **Target**: A column named `DefectStatus` with binary values (e.g., `0` for no defect, `1` for defect).
2. Input data for prediction must include all 16 parameters.

---

## Setup Instructions

### Prerequisites
- Python 3.10 or later
- Required libraries: `fastapi`, `joblib`, `pandas`, `scikit-learn`, `pydantic`, `uvicorn`

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/thor-x-me/AssignmentTechPranee.git
   cd AssignmentTechPranee
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Run the Application
1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
2. Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs) (This link will work only when the main.py script is running).

---

## How It Works
1. **Upload**: Upload a CSV dataset provided in the repository.
2. **Train**: The API splits the data, scales the features, and trains a Decision Tree Classifier.
3. **Predict**: Provide feature inputs to predict whether a product is defective.

---

## Error Handling
- **File Errors**: If the uploaded file is invalid or not a CSV, the API returns a `400` error.
- **Training Errors**: If training fails due to missing data or incorrect file format, the API returns a `500` error.
- **Prediction Errors**: If prediction fails due to missing or incorrect inputs, the API returns a `500` error.

---

## Author
Developed by **Abhishek Verma**.