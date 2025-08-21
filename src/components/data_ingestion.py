import os
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTrans

@dataclass
class DataIngestionConfig:  
    train_data = os.path.join('artifacts', 'train.csv')
    test_data = os.path.join('artifacts', 'test.csv')
    raw_data = os.path.join('artifacts','data.csv')
    
class DataIngestion: 
    def __init__(self):
        self.ingestion = DataIngestionConfig()
        
    def start(self):
        logging.info('Data Ingestion Component was initialized!')
        try: 
            df = pd.read_csv(r'D:\Projects\Data Science Project\Current\dsproject\notebook\data\WA_Fn-UseC_-Telco-Customer-Churn.csv')

            logging.info('Dataframe initialized using the dataset!')
            
            os.makedirs(os.path.dirname(self.ingestion.raw_data), exist_ok=True) 
            
            df.to_csv(self.ingestion.raw_data, index =False, header=True)
            
            logging.info('Train-Test split started!')
            
            train, test = train_test_split(df, test_size=0.3, random_state=42)
            
            logging.info(f'Train Data stored in {self.ingestion.train_data} as {os.path.basename(self.ingestion.train_data)}')
            train.to_csv(self.ingestion.train_data, index = False, header=True)
            
            logging.info(f'Test Data stored in {self.ingestion.test_data} as {os.path.basename(self.ingestion.test_data)}')
            test.to_csv(self.ingestion.test_data, index = False, header=True)
            
            logging.info("Data ingestion completed")
            
            return (self.ingestion.train_data, self.ingestion.test_data)
            
            
        except Exception as e: 
            logging.exception('Data ingestion failed!')
            raise CustomException("Data ingestion failed!") from e
    
if __name__ == "__main__":
    x = DataIngestion()
    train, test = x.start()
    
    y = DataTrans()
    y.start(train, test)