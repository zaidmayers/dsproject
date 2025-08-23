import sys
import os
import pandas as pd
from src.exception import CustomException
from src.utils import load_object

class PredictPipeline:
    def __init__(self):
        pass
    
    def predict(self, features):
        try:
            model_path= os.path.join('artifacts', 'model.joblib')
            preprocessor_path = os.path.join('artifacts', 'preprocessor.joblib')
            model = load_object(model_path)
            preprocessor = load_object(preprocessor_path)
            data = preprocessor.transform(features)
            predictions = model.predict(data)
            return predictions
        
        except Exception as e:
            raise CustomException(e)

class AcquireData():
    
    def __init__(self,
        gender: str,
        SeniorCitizen: int,
        Partner: str,
        Dependents: str,
        tenure: int,
        PhoneService: str,
        MultipleLines: str,
        InternetService: str,
        OnlineSecurity: str,
        OnlineBackup: str,
        DeviceProtection: str,
        TechSupport: str,
        StreamingTV: str,
        StreamingMovies: str,
        Contract: str,
        PaperlessBilling: str,
        PaymentMethod: str,
        MonthlyCharges: float,
        TotalCharges: float):

        self.gender = gender
        self.SeniorCitizen = SeniorCitizen
        self.Partner = Partner
        self.Dependents = Dependents
        self.tenure = tenure
        self.PhoneService = PhoneService
        self.MultipleLines = MultipleLines
        self.InternetService = InternetService
        self.OnlineSecurity = OnlineSecurity
        self.OnlineBackup = OnlineBackup
        self.DeviceProtection = DeviceProtection
        self.TechSupport = TechSupport
        self.StreamingTV = StreamingTV
        self.StreamingMovies = StreamingMovies
        self.Contract = Contract
        self.PaperlessBilling = PaperlessBilling
        self.PaymentMethod = PaymentMethod
        self.MonthlyCharges = MonthlyCharges
        self.TotalCharges = TotalCharges


    def create_df(self):
        try: 
            input = {
            "gender": [self.gender],
            "SeniorCitizen": [self.SeniorCitizen],
            "Partner": [self.Partner],
            "Dependents": [self.Dependents],
            "tenure": [self.tenure],
            "PhoneService": [self.PhoneService],
            "MultipleLines": [self.MultipleLines],
            "InternetService": [self.InternetService],
            "OnlineSecurity": [self.OnlineSecurity],
            "OnlineBackup": [self.OnlineBackup],
            "DeviceProtection": [self.DeviceProtection],
            "TechSupport": [self.TechSupport],
            "StreamingTV": [self.StreamingTV],
            "StreamingMovies": [self.StreamingMovies],
            "Contract": [self.Contract],
            "PaperlessBilling": [self.PaperlessBilling],
            "PaymentMethod": [self.PaymentMethod],
            "MonthlyCharges": [self.MonthlyCharges],
            "TotalCharges": [self.TotalCharges],
        }
            return pd.DataFrame(input)
        
        except Exception as e: 
            raise CustomException
            
