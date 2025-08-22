import os
import sys
from dataclasses import dataclass
os.environ["LOKY_MAX_CPU_COUNT"] = "8"
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
import warnings
warnings.filterwarnings('ignore')
from src.exception import CustomException
from src.logger import logging
from src.components.data_transformation import DataTrans
from src.components.data_ingestion import DataIngestion
from src.utils import save_object, evaluate

@dataclass
class ModelTrainConfig:
    trainer = os.path.join('artifacts', 'model.joblib')
    
class ModelTrainer:
    def __init__(self):
        self.config = ModelTrainConfig()
        
    def start(self, train_arr, test_arr): 
        try:
            logging.info('Allocating the train and test split.')
            X_train, X_test, y_train, y_test = (
                train_arr[:,:-1], 
                test_arr[:,:-1], 
                train_arr[:,-1], 
                test_arr[:,-1]
                )

            n = (y_train == 0).sum()
            p = (y_train == 1).sum()
            xgb_scale = n/p
            total = n + p
            w0 = total/(2*n)
            w1 = total/(2*p)

            models = {
                "Logistic Regression": LogisticRegression(),
                "K-Neighbors Classifier": KNeighborsClassifier(),
                "Decision Tree": DecisionTreeClassifier(),
                "Random Forest": RandomForestClassifier(),
                "XGBClassifier": XGBClassifier(),
                "CatBoostClassifier": CatBoostClassifier(class_weights=[w0, w1], verbose=False),
                "AdaBoost Classifier": AdaBoostClassifier()
            }
            params = {
            "Logistic Regression": {
                "C": [0.01, 0.1, 1, 10], 
                "penalty": ["l2"],         
                "solver": ["liblinear", "saga"],
                "class_weight": ["balanced"]
            },
            "K-Neighbors Classifier": {
                "n_neighbors": [3, 5, 7, 9],
                "weights": ["uniform", "distance"],
                "metric": ["minkowski", "euclidean", "manhattan"]
            },
            "Decision Tree": {
                "max_depth": [3, 5, 10, None],
                "min_samples_split": [2, 5, 10],
                "criterion": ["gini", "entropy"]
            },
            "Random Forest": {
                "n_estimators": [50, 100, 200],
                "max_depth": [5, 10, None],
                "min_samples_split": [2, 5, 10],
                "class_weight": ["balanced"]
            },
            "XGBClassifier": {
                "n_estimators": [100, 200],
                "learning_rate": [0.01, 0.1, 0.2],
                "max_depth": [3, 5, 7],
                "scale_pos_weight": [xgb_scale]  
            },
            "CatBoostClassifier": {
                "depth": [6, 8, 10],
                "learning_rate": [0.01, 0.05, 0.1],
                "iterations": [50, 100, 200],
            },
            "AdaBoost Classifier": {
                "n_estimators": [50, 100, 200],
                "learning_rate": [0.01, 0.1, 1]
            }}
            
            scores = evaluate(X_train,y_train,X_test,y_test,models,params)
            best_model_name = max(scores, key=scores.get)
            best_model_score = scores[best_model_name]
                
            if best_model_score <0.6:
                raise CustomException("A good enough model doesn't exist.")
            
            save_object(models[best_model_name], self.config.trainer) 
            logging.info(f"Model with maximum f1 score saved.")
            return best_model_score
        
        except Exception as e: 
            raise CustomException(e)
        
        
if __name__ == "__main__":
    x = DataIngestion()
    train, test = x.start()
    
    y = DataTrans()
    train_arr, test_arr, _ = y.start(train, test)
    
    trainer = ModelTrainer()
    print(trainer.start(train_arr, test_arr))