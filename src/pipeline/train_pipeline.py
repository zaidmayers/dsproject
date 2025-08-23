from src.exception import CustomException
from src.logger import logging
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTrans
from src.components.model_trainer import ModelTrainer

class TrainingPipeline:
    def __init__(self):
        self.ingestion = DataIngestion()
        self.transformation = DataTrans()
        self.trainer = ModelTrainer()
        
    def run(self):
        try: 
            logging.info('Training Pipeline Initiated!')
            
            train_df, test_df = self.ingestion.start()
            
            trans_train_df, trans_test_df = self.transformation.start(train_df, test_df)
            
            score = self.trainer.start(trans_train_df, trans_test_df)
            
            logging.info("Training Pipeline Completed!")
            return score
            
        except Exception as e:
            logging.error("Error occurred during training pipeline.")
            raise CustomException(e)


if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.run()