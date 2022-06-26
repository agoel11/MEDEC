# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 20:46:36 2020

@author: Atharva
"""

symptoms = ['itching',
 'skin rash',
 'nodal skin eruptions',
 'continuous sneezing',
 'shivering',
 'chills',
 'joint pain',
 'stomach pain',
 'acidity',
 'ulcers on tongue',
 'muscle wasting',
 'vomiting',
 'burning micturition',
 'spotting  urination',
 'fatigue',
 'weight gain',
 'anxiety',
 'cold hands and feets',
 'mood swings',
 'weight loss',
 'restlessness',
 'lethargy',
 'patches in throat',
 'irregular sugar level',
 'cough',
 'high fever',
 'sunken eyes',
 'breathlessness',
 'sweating',
 'dehydration',
 'indigestion',
 'headache',
 'yellowish skin',
 'dark urine',
 'nausea',
 'loss of appetite',
 'pain behind the eyes',
 'back pain',
 'constipation',
 'abdominal pain',
 'diarrhoea',
 'mild fever',
 'yellow urine',
 'yellowing of eyes',
 'acute liver failure',
 'fluid overload',
 'swelling of stomach',
 'swelled lymph nodes',
 'malaise',
 'blurred and distorted vision',
 'phlegm',
 'throat irritation',
 'redness of eyes',
 'sinus pressure',
 'runny nose',
 'congestion',
 'chest pain',
 'weakness in limbs',
 'fast heart rate',
 'pain during bowel movements',
 'pain in anal region',
 'bloody stool',
 'irritation in anus',
 'neck pain',
 'dizziness',
 'cramps',
 'bruising',
 'obesity',
 'swollen legs',
 'swollen blood vessels',
 'puffy face and eyes',
 'enlarged thyroid',
 'brittle nails',
 'swollen extremeties',
 'excessive hunger',
 'extra marital contacts',
 'drying and tingling lips',
 'slurred speech',
 'knee pain',
 'hip joint pain',
 'muscle weakness',
 'stiff neck',
 'swelling joints',
 'movement stiffness',
 'spinning movements',
 'loss of balance',
 'unsteadiness',
 'weakness of one body side',
 'loss of smell',
 'bladder discomfort',
 'foul smell of urine',
 'continuous feel of urine',
 'passage of gases',
 'internal itching',
 'toxic look (typhos)',
 'depression',
 'irritability',
 'muscle pain',
 'altered sensorium',
 'red spots over body',
 'belly pain',
 'abnormal menstruation',
 'dischromic  patches',
 'watering from eyes',
 'increased appetite',
 'polyuria',
 'family history',
 'mucoid sputum',
 'rusty sputum',
 'lack of concentration',
 'visual disturbances',
 'receiving blood transfusion',
 'receiving unsterile injections',
 'coma',
 'stomach bleeding',
 'distention of abdomen',
 'history of alcohol consumption',
 'fluid overload.1',
 'blood in sputum',
 'prominent veins on calf',
 'palpitations',
 'painful walking',
 'pus filled pimples',
 'blackheads',
 'scurring',
 'skin peeling',
 'silver like dusting',
 'small dents in nails',
 'inflammatory nails',
 'blister',
 'red sore around nose',
 'yellow crust ooze']


diagnosis = ['Paroymsal Vertigo',
 'AIDS',
 'Acne',
 'Alcoholic hepatitis',
 'Allergy',
 'Arthritis',
 'Bronchial Asthma',
 'Cervical spondylosis',
 'Chicken pox',
 'Chronic cholestasis',
 'Common Cold',
 'Dengue',
 'Diabetes ',
 'Piles',
 'Drug Reaction',
 'Fungal infection',
 'GERD',
 'Gastroenteritis',
 'Heart attack',
 'Hepatitis B',
 'Hepatitis C',
 'Hepatitis D',
 'Hepatitis E',
 'Hypertension ',
 'Hyperthyroidism',
 'Hypoglycemia',
 'Hypothyroidism',
 'Impetigo',
 'Jaundice',
 'Malaria',
 'Migraine',
 'Osteoarthristis',
 'Brain Hemorrhage',
 'Peptic Ulcers',
 'Pneumonia',
 'Psoriasis',
 'Tuberculosis',
 'Typhoid',
 'Urinary Tract Infection',
 'Varicose veins',
 'hepatitis A']

dangerous = ['Piles',
 'Heart attack',
 'Jaundice',
 'Malaria',
 'Brain Hemorrhage',
 'Pneumonia',
 'Psoriasis',
 'Tuberculosis',
 'Typhoid']

from flask import Flask, render_template
from flask import request
import tensorflow as tf
import numpy as np

def get_input_model(symptoms_list):
    
    symptomsidx = []
    
    for x in symptoms_list:
        symptomsidx.append(symptoms.index(x))
    symptoms_model = np.zeros((1, 132))

    for x in symptomsidx:
        symptoms_model[0, x] = 1
    print(symptoms_model)
    return symptoms_model


model =  tf.keras.models.load_model('model.h5')
def get_model_results(symptoms_model):
    results = model.predict(symptoms_model)

    sum = np.sum(results)
    results_percent = []
    for x in results:
        results_percent.append(x/sum)

    results_percent = results_percent[0].tolist()
    dict_results = {}
    temp = results_percent
    for x in range(4):
        percent = max(temp)
        idx = results_percent.index(percent)
        disease = diagnosis[idx]
        
        dict_results["disease" + str(x+1)] = disease
        dict_results["percent" + str(x+1)] = percent

        temp.remove(percent)
    

    return dict_results


def link_finder(disease):
    og_link = "https://search.cdc.gov/search/?query="
    new_link = og_link + disease
    return new_link


application = Flask(__name__)

@application.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", symptoms=" ".join(symptoms))

@application.route('/search', methods=['GET', 'POST'])
def search():
    print(request.method)
    if request.method == 'POST':
        print(request.form)
    
    symptoms_list = request.form["symptoms"].split("~")[1:]
    results = get_model_results(get_input_model(symptoms_list))





    return render_template("search.html", bad_list=" ".join(dangerous), diseasename1 = results["disease1"], diseasename2 = results["disease2"], diseasename3 = results["disease3"], diseasename4 = results["disease4"], link1 = link_finder(results["disease1"]), link2 = link_finder(results["disease2"]), link3 = link_finder(results["disease3"]), link4 = link_finder(results["disease4"]), percentmatch1 = round(results["percent1"]*100, 2), percentmatch2 = round(results["percent2"]*100, 2), percentmatch3 = round(results["percent3"]*100, 2), percentmatch4 = round(results["percent4"]*100, 2))


# run the application.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
