import os
from src.exception import CustomException
from src.logger import logging
import joblib
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score

def save_object(obj, filename):
    try: 
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        joblib.dump(obj, filename)
        logging.info(f'Object succsessfully saved to: {filename}')
        return True
        
    except Exception as e: 
        logging.exception('Joblib object saving failed!')
        raise CustomException(f'Error saving object to {filename} as {e}')
    
def evaluate(X_train, y_train,X_test,y_test,models,params):
    try:
        performance_records = {}
        logging.info('Selecting model and training with best parameters.')
        for name, model in models.items():
            param = params.get(name, {})
            
            gscv = GridSearchCV(model, param, cv=3, scoring="f1")
            gscv.fit(X_train, y_train)
            
            best_model = gscv.best_estimator_
            
            y_pred_test = best_model.predict(X_test)
            test_model_score = f1_score (y_test, y_pred_test)
            
            performance_records[name] = test_model_score
        logging.info('Test records from models trained are saved.')
        return performance_records
    
    except Exception as e:
        raise CustomException(e)