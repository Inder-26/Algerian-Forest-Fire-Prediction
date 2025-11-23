import pickle
from flask import Flask,render_template,request
import numpy as np

application = Flask(__name__)
app=application

# --- Model Loading ---
try:
    ridge_model=pickle.load(open('models/ridge.pkl','rb'))
    standard_scaler=pickle.load(open('models/scalar.pkl','rb'))
    MODELS_LOADED = True
except Exception as e:
    MODELS_LOADED = False
    ridge_model = None
    standard_scaler = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if not MODELS_LOADED:
        return render_template('home.html', results="Error: Prediction models could not be loaded.", fwi_result=None)
        
    if request.method=="POST":
        try:
            # Data extraction
            Temperature = float(request.form.get('Temperature'))
            RH = float(request.form.get('RH'))
            Ws = float(request.form.get('Ws'))
            Rain = float(request.form.get('Rain'))
            FFMC = float(request.form.get('FFMC'))
            DMC = float(request.form.get('DMC'))
            ISI = float(request.form.get('ISI'))
            Region = float(request.form.get('Region'))

            # Prepare data and predict
            input_data = np.array([[Temperature, RH, Ws, Rain, FFMC, DMC, ISI, Region]])
            input_scaled = standard_scaler.transform(input_data)
            result = ridge_model.predict(input_scaled)
            
            return render_template('home.html', results="Success", fwi_result=result[0])
            
        except ValueError:
            error_message = "Invalid input. All fields must be valid numbers."
            return render_template('home.html', results=error_message, fwi_result=None)
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"
            return render_template('home.html', results=error_message, fwi_result=None)
            
    else:
        # GET Request
        return render_template('home.html', results=None, fwi_result=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)