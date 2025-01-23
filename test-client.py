import time

import gradio as gr
import requests
import pandas as pd
import json


class ManufacturingPredictorClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def upload_data(self, file_path):
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(f"{self.base_url}/upload", files=files)
        response.raise_for_status()
        return response.json()

    def train_model(self):
        response = requests.post(f"{self.base_url}/train")
        response.raise_for_status()
        return response.json()

    def predict(self, input_data):
        try:
            response = requests.post(f"{self.base_url}/predict", json=input_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {e}")
            print(f"Response content: {e.response.text if e.response else 'No response'}")
            raise


# Create API client
client = ManufacturingPredictorClient()

print("This is a simpel demo:")
train_choice = input("Do you want to train the model?\nChoose yes if you are running this for first time: (y/n)")
if train_choice == "y" or train_choice == 'Y':
    file_path = input("Enter trainng data file:")
    responce = client.upload_data(file_path)
    print(responce)
    if responce:
        client.train_model()
    else:
        print("Error in file or trainng process.")
print("Input data row to predict.")
in_data = input("Data:").split(',')
data = {
    'ProductionVolume': float(in_data[0]),
    'ProductionCost': float(in_data[1]),
    'SupplierQuality': float(in_data[2]),
    'DeliveryDelay': float(in_data[3]),
    'DefectRate': float(in_data[4]),
    'QualityScore': float(in_data[5]),
    'MaintenanceHours': float(in_data[6]),
    'DowntimePercentage': float(in_data[7]),
    'InventoryTurnover': float(in_data[8]),
    'StockoutRate': float(in_data[9]),
    'WorkerProductivity': float(in_data[10]),
    'SafetyIncidents': float(in_data[11]),
    'EnergyConsumption': float(in_data[12]),
    'EnergyEfficiency': float(in_data[13]),
    'AdditiveProcessTime': float(in_data[14]),
    'AdditiveMaterialCost': float(in_data[15])
}
print(data)
result = client.predict(data)
print(result)

