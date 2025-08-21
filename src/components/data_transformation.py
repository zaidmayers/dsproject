import os
import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransConfig: 
    preprocessor = os.path.join('artifacts', 'preprocessor.joblib')
    
class DataTrans: 
    def __init__(self):
        self.config = DataTransConfig()
        
    def transformer(self):
        try:
            logging.info('Data Transformer initialized.')
            logging.info('Numerical and Categorical Features loading in.')
            
            numerical_features = ['tenure', 'MonthlyCharges', 'TotalCharges']
            categorical_features = ['InternetService', 'DeviceProtection', 'TechSupport', 'PaperlessBilling', 'Contract', 'OnlineBackup', 'gender', 'StreamingMovies', 'PaymentMethod', 'SeniorCitizen', 'PhoneService', 'MultipleLines', 'Dependents', 'Partner', 'StreamingTV', 'OnlineSecurity']
            
            numerical_imputer = SimpleImputer(strategy='median')
            scaler = StandardScaler()

            numerical_pipeline = Pipeline(
                steps = [
                    ('imputer', numerical_imputer), 
                    ('scaler', scaler)
                    ]
                )

            logging.info("Numerical columns imputed and standard scaling completed.")
            
            categorical_imputer = SimpleImputer(strategy='most_frequent')
            encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

            categorical_pipeline = Pipeline(
                steps = [
                    ('imputer', categorical_imputer),
                    ('encoder', encoder)
                    ]
                )

            logging.info("Categorical columns imputed and OneHot encoding completed.")

            preprocessor = ColumnTransformer(
                transformers = [
                    ('num_trans', numerical_pipeline, numerical_features), 
                    ('cat_trans', categorical_pipeline, categorical_features)
                    ]
                )    

            return preprocessor
        
        except Exception as e: 
            logging.exception('Data transformation failed!')
            raise CustomException("Data ingestion failed!") from e
        
    def start(self, train, test): 
        try: 
            target = "Churn"
            outlier = "TotalCharges"

            train = pd.read_csv(train).dropna(subset=[target])
            train[outlier] = pd.to_numeric(train[outlier], errors='coerce')
            train[outlier].fillna(train[outlier].median(), inplace=True)
            
            test = pd.read_csv(test).dropna(subset=[target])
            test[outlier] = pd.to_numeric(test[outlier], errors='coerce')
            test[outlier].fillna(test[outlier].median(), inplace=True)
            
            logging.info("Reading in training and testing data as dataframes.")
            
            preprocessor = self.transformer()            
            
            train_features = train.drop(columns=[target], axis=1)
            train_target = train[target].map({"No":0, "Yes":1}).astype(int)
            
            test_features = test.drop(columns=[target], axis=1)
            test_target = test[target].map({"No":0, "Yes":1}).astype(int)
            
            logging.info('Applying the transformer on the train and test dataframes.')
            
            training_input_features = preprocessor.fit_transform(train_features)
            testing_input_features = preprocessor.transform(test_features)
            
            
            train_arr = np.c_[training_input_features, np.array(train_target)]
            
            test_arr = np.c_[testing_input_features, np.array(test_target)]
            
            logging.info('Tranformed data stored as arrays.')
            
            save_object(preprocessor, self.config.preprocessor)
            
            return (train_arr, test_arr, self.config)
        except Exception as e: 
            raise CustomException(e)