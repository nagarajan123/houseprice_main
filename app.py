from flask import Flask, render_template, request, url_for, Response
import json
import requests
import numpy as np
import pickle


app = Flask(__name__)

model = pickle.load(open('banglore_home_price_model.pickle', 'rb'))

with open('columns.json', 'r') as f:
    col = json.load(f)['data_columns']



def prediction_of_house(location, sqft, bath, bhk):
    i = -1
    for l in col:
        i = i + 1
        if l == location:
            loc_index = i
    
    z = np.zeros(len(col))
    z[0] = sqft
    z[1] = bath
    z[2] = bhk
    if loc_index >= 0:
        z[loc_index] = 1
    return round(model.predict([z])[0], 2)



# print(col[4:])

@app.route('/')
def home():
    return render_template('home.html', columns = col[4:])


@app.route('/predict_price', methods = ['POST'])
def prediction():  
    loc = request.form['location']
    sqft = request.form['sqft']
    bath = request.form['bath']
    bhk = request.form['bhk']

    predicted_price = prediction_of_house(loc, sqft, bath, bhk)

    return render_template('home.html', result = "Price of House : "+str(predicted_price)+" Lac", columns = col[4:])


if __name__ == '__main__':
    app.run(debug=True)