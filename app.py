import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
from model import cd
import sqlite3

app = Flask(__name__)

model = pickle.load(open('model/model.pkl', 'rb'))

@app.route("/")
def intro():
    return render_template('intro.html')

@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')

@app.route("/signup")
def signup():

    username = request.args.get('user','')
    name = request.args.get('name','')
    email = request.args.get('email','')
    number = request.args.get('mobile','')
    password = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
    con.commit()
    con.close()
    return render_template("signin.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")    

    elif mail1 == 'admin' and password1 == 'admin':
        return render_template("index.html")

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("index.html")
    else:
        return render_template("signup.html")


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    com_fea=['Area',                                                                 
                'percent_of_production',                     
                'State_Name_Andaman and Nicobar Islands',   
                'State_Name_Andhra Pradesh',                 
                'State_Name_Arunachal Pradesh',             
                'Season_Autumn',                        
                'Season_Kharif',                            
                'Season_Rabi',                               
                'Season_Whole Year',                         
                'Crop_Arecanut',                             
                'Crop_Arhar/Tur',                            
                'Crop_Bajra',                                
                'Crop_Banana',                              
                'Crop_Beans & Mutter(Vegetable)',            
                'Crop_Bhindi',                              
                'Crop_Black pepper',                         
                'Crop_Bottle Gourd',                         
                'Crop_Brinjal',                             
                'Crop_Cabbage',                              
                'Crop_Cashewnut',                            
                'Crop_Castor seed',                          
                'Crop_Citrus Fruit',                         
                'Crop_Coconut',                              
                'Crop_Coriander',                            
                'Crop_Cotton(lint)',                         
                'Crop_Cowpea(Lobia)',                        
                'Crop_Cucumber',                             
                'Crop_Dry chillies',                         
                'Crop_Dry ginger',                           
                'Crop_Garlic',                               
                'Crop_Ginger',                              
                'Crop_Gram',                                 
                'Crop_Grapes',                               
                'Crop_Groundnut',                            
                'Crop_Horse-gram',                           
                'Crop_Jowar',                                
                'Crop_Korra',                                
                'Crop_Lemon',                                
                'Crop_Linseed',                              
                'Crop_Maize',                                
                'Crop_Mango',                                
                'Crop_Masoor',                               
                'Crop_Mesta',                                
                'Crop_Moong(Green Gram)',                    
                'Crop_Niger seed',                           
                'Crop_Oilseeds total',                       
                'Crop_Onion',                                
                'Crop_Orange',                               
                'Crop_Other  Rabi pulses',                  
                'Crop_Other Fresh Fruits',                   
                'Crop_Other Kharif pulses',                  
                'Crop_Other Vegetables',
                'Crop_Papaya',                               
                'Crop_Peas  (vegetable)',
                'Crop_Pome Fruit',                           
                'Crop_Pome Granet',                         
                'Crop_Potato',                              
                'Crop_Pulses total',                         
                'Crop_Ragi',                                 
                'Crop_Rapeseed &Mustard',                    
                'Crop_Rice',                                 
                'Crop_Safflower',                            
                'Crop_Samai',                                
                'Crop_Sapota',                               
                'Crop_Sesamum',                              
                'Crop_Small millets',                        
                'Crop_Soyabean',                             
                'Crop_Sugarcane',                            
                'Crop_Sunflower',                            
                'Crop_Sweet potato',                        
                'Crop_Tapioca',                              
                'Crop_Tobacco',                              
                'Crop_Tomato',                               
                'Crop_Turmeric',                             
                'Crop_Urad',                                 
                'Crop_Varagu',                               
                'Crop_Wheat',                                
                'Crop_other fibres',                         
                'Crop_other misc. pulses',                   
                'Crop_other oilseeds'                       ]


    dataf=pd.DataFrame(columns=com_fea)
    dataf.loc[len(dataf)]=0
    
    
    features = [x for x in request.form.values()] #state | season | crop | area
    dataf['Area']=float(features[3])
    
    for j in com_fea:
        test_list=j.strip().split('_')
        
        if (test_list[0]=='State'):
            if(test_list[-1]==features[0]):
                dataf[j]=1
                
        elif (test_list[0]=='Season'):
            if(test_list[-1]==features[1]):
                dataf[j]=1
                
        elif (test_list[0]=='Crop'):            
            if(test_list[-1]==features[2]):
                dataf[j]=1
                    
    
    prediction = model.predict(dataf)
    print(prediction)
    output = round(prediction[0], 2)


    return render_template('result.html', prediction_text='Predicted rate = {}'.format(output))


if __name__ == "__main__":
 app.run(host='127.0.0.1', port=5000,debug=True)