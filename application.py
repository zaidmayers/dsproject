from flask import Flask, request, render_template
from src.pipeline.predict_pipeline import PredictPipeline, AcquireData
import os
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        data = AcquireData(
                            gender=request.form.get('gender'),
                            SeniorCitizen=int(request.form.get('SeniorCitizen')),
                            Partner=request.form.get('Partner'),
                            Dependents=request.form.get('Dependents'),
                            tenure=int(request.form.get('tenure')),
                            PhoneService=request.form.get('PhoneService'),
                            MultipleLines=request.form.get('MultipleLines'),
                            InternetService=request.form.get('InternetService'),
                            OnlineSecurity=request.form.get('OnlineSecurity'),
                            OnlineBackup=request.form.get('OnlineBackup'),
                            DeviceProtection=request.form.get('DeviceProtection'),
                            TechSupport=request.form.get('TechSupport'),
                            StreamingTV=request.form.get('StreamingTV'),
                            StreamingMovies=request.form.get('StreamingMovies'),
                            Contract=request.form.get('Contract'),
                            PaperlessBilling=request.form.get('PaperlessBilling'),
                            PaymentMethod=request.form.get('PaymentMethod'),
                            MonthlyCharges=float(request.form.get('MonthlyCharges')),
                            TotalCharges=float(request.form.get('TotalCharges'))
                            )
        df = data.create_df()
        
        pipe = PredictPipeline()
        result = pipe.predict(df)

        prediction_label = "The customer will Churn" if result[0] == 1 else "No Churn"

        return render_template('home.html', result=prediction_label)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
    