from flask import Flask, request, render_template
import pandas as pd
import h2o
from h2o.automl import H2OAutoML
h2o.init(max_mem_size='2G')

app = Flask("__name__")

df = pd.read_csv('Water_potability_refined.csv')
model_path = '/Users/Anushka/Desktop/water_quality_prediction/StackedEnsemble_AllModels_3_AutoML_1_20240730_230141'

q= ""

@app.route("/")
def loadPage():
	return render_template('index.html', query="")

@app.route("/", methods=['POST'])

def predict():
	

    inputQuery1 = request.form['query1']
    inputQuery2 = request.form['query2']
    inputQuery3 = request.form['query3']
    inputQuery4 = request.form['query4']
    inputQuery5 = request.form['query5']
    inputQuery6 = request.form['query6']
    inputQuery7 = request.form['query7']
    inputQuery8 = request.form['query8']
    inputQuery9 = request.form['query9']

    model = h2o.load_model(model_path)

    data=[[inputQuery1, inputQuery2, inputQuery3, inputQuery4, inputQuery5, inputQuery6, inputQuery7, inputQuery8, inputQuery9]]

    new_df = pd.DataFrame(data, columns = ['pH','Hardness','Solids','Chloramines','Sulfate','Conductivity',
                                           'Organic_carbon','Trihalomethanes','Turbidity'] )
    new_h2o_df = h2o.H2OFrame(new_df)

    prediction = model.predict(new_h2o_df)

    predict_values = prediction['predict'].as_data_frame()

    predicted_class = predict_values.iloc[0, 0]

    confidence_0 = prediction['p0'].as_data_frame()

    confidence_0_class = confidence_0.iloc[0,0]

    confidence_1 = prediction['p1'].as_data_frame()
    
    confidence_1_class = confidence_1.iloc[0,0]

    if predicted_class==0:
          o1 = "The water is not potable"
          o2 = "Confidence {}".format(confidence_0_class*100)
    else:
          o1 = "The water is potable"
          o2 = "Confidence {}".format(confidence_1_class*100)
    
    return render_template('index.html', output1=o1, output2=o2, 
                        query1 = request.form['query1'], 
                        query2 = request.form['query2'],
                        query3 = request.form['query3'],
                        query4 = request.form['query4'],
                        query5 = request.form['query5'], 
                        query6 = request.form['query6'], 
                        query7 = request.form['query7'], 
                        query8 = request.form['query8'], 
                        query9 = request.form['query9'])

app.run(debug=True,port=5002)


