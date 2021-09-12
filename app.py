from flask import Flask,render_template,request,jsonify
import numpy as np
import pickle

app = Flask(__name__)
model = pickle.load(open('model5.pkl','rb'))

@app.route('/', methods=['GET', 'POST']) # To render Homepage
def home_page():
    return render_template('index.html')


def agedetector(age):
    if age >=0 and age <=17:
        return 1
    elif age >=18 and age <=29:
        return 2
    elif age >=30 and age <=49:
        return 3
    elif age >=50 and age <=69:
        return 4
    else:
        return 5            


def disease_predictor(disease):
    if disease == 'Short gestation; low birth weight; and fetal growth retardation':
        return 5
    elif disease == 'Respiratory distress syndrome':
        return 4
    elif disease == 'Tuberculosis':
        return 3
    elif disease == 'Leukemias':
        return 2
    else:
        return 1

def genderPredictor(Gender):
    if Gender == 'Female':
        return [1,0,0]
    elif Gender == 'Male':
        return [0,1,0]
    else:
        return [0,0,1]


def zipvalueestimator(Zip):
     if Zip == '100': 
         return 74696.827231
     elif Zip == '101':
         return 84605.396971 
     elif Zip == '103':
         return 69452.579158
     else:
         return 34690.563752
 








@app.route('/lengthofstay', methods=['POST'])  # This will be called from UI
def math_operation():
    if (request.method=='POST'):
        try:


            
            charges=(request.form['charges'])
            Illness_code =request.form['Illness_code']
            Mortality =request.form['Mortality']
            Age = int(request.form['Age'])
            Zip = str(request.form['Zip'])
            Disease = str(request.form['Disease'])
            Gender =str(request.form['Gender'])

            Age = agedetector(Age)
            zip_value = zipvalueestimator(Zip)
            Disease = disease_predictor(Disease)
            Gender = genderPredictor(Gender)

            int_features = []
            int_features.append(int(charges))
            int_features.append(int(Illness_code))
            int_features.append(int(Mortality))
            int_features.append(Age)
            int_features.append(zip_value)
            int_features.append(Disease)
            # int_features.extend(Gender)

            print(int_features)

            

            final_features = [np.array(int_features)]

            



            prediction = int(model.predict(final_features))

            return render_template('results.html',result=prediction) 
        except:

            return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)          