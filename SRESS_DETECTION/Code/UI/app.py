from flask import Flask,render_template,request,session, url_for, redirect,jsonify
#from flask_mysqldb import MySQL
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import os
import pickle
import pymysql
import numpy as np
from sklearn.linear_model import LogisticRegression # Logistic Regression
import joblib
import pandas as pd #
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn.preprocessing import RobustScaler
from sklearn.neighbors import KNeighborsRegressor  
from sklearn.metrics import mean_squared_error,r2_score
from werkzeug.utils import secure_filename
# from urllib import request

def dbConnection():
    connection = pymysql.connect(host="localhost", user="root", password="root", database="stressdection")
    return connection

def dbClose():
    dbConnection().close()
    return


app=Flask(__name__)
app.secret_key = 'random string'
app.config['UPLOADED_PHOTOS_DEST'] = 'static/Profile/'
 
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/SessionHandle1',methods=['POST','GET'])
def SessionHandle1():
    if request.method == "POST":
        details = request.form
        name = details['name']
        session['name'] = name
        strofuser = name
        print (strofuser.encode('utf8', 'ignore'))
        return strofuser    



@app.route('/')
def index():

    
    return render_template('index.html')



@app.route('/home')
def home():
    
    return render_template('home.html')



@app.route('/searchvideo',methods=['POST','GET'])
def searchvideo():
    return render_template('search.html')


@app.route('/transaction',methods=['POST','GET'])
def transaction():
    if request.method == "POST":
       print("===============================================")
      
       f = request.files['file']
       basepath = os.path.dirname(__file__)
       input_csv_path = os.path.join(basepath, 'static/uploads', secure_filename(f.filename))
       f.save(input_csv_path)
        # Read the CSV file into a DataFrame
       print("===============================================")
       

       df=pd.read_csv(input_csv_path)
      
      
      
       print("-------------------------------Model Load------------------------------------------------")
       new_list=[]
       filename='model/DecisionTreeClassifier_pickle'
       loaded_model_rf = pickle.load(open(filename, 'rb'))
       rf1=loaded_model_rf.predict(df)
       output_model=rf1[0]

       print("-------------------------------------------------------------------------------")
       print(output_model)
       print("-------------------------------------------------------------------------------")
       
       

      
        # labels = {0: "Amused",1: "Neutral",2: "Stressed"}
        
       if output_model == 0:
            print("Amused")
            pred="Amused"
            message = "The user is  Amused"   
            print(message)
            return jsonify({'message': message,'pred': pred})
            
       elif output_model == 1:
            print("Neutral")
            pred="Neutral"
            message = "The user is Neutral."
            print(message)  
            return jsonify({'message': message,'pred': pred})
       else:
            print("Stressed")
            pred="Stressed"
            message = "The user is affected by Stressed."
            print(message)
            return jsonify({'message': message,'pred': pred})

     
    return render_template('detection.html')

@app.route('/register',methods=['POST','GET'] )
def register():
    if request.method == "POST":
        try:
            status=""
            fname = request.form.get("name")
            add = request.form.get("add")
            pno = request.form.get("pno")
            email = request.form.get("email")
            pass1 =  request.form.get("pass")
            f2 = request.files['file']
            
            con = dbConnection()
            cursor = con.cursor()
            cursor.execute('SELECT * FROM userdetailes WHERE email = %s', (email))
            res = cursor.fetchone()
            #res = 0
            if not res:
                filename_secure = secure_filename(f2.filename)
                f2.save(os.path.join(
                   app.config['UPLOADED_PHOTOS_DEST'], filename_secure))
                filenamepath = os.path.join(
                   app.config['UPLOADED_PHOTOS_DEST'], filename_secure)
                print("filenamepath", filenamepath)
                
                sql = "INSERT INTO userdetailes (name, address,phone,email,password,filenamepath) VALUES (%s,%s, %s, %s, %s, %s)"
                val = (fname ,add ,pno ,email ,pass1,filenamepath)
                print(sql," ",val)
                cursor.execute(sql, val)
                con.commit()
                status= "success"
                return render_template("login.html")
            else:
                status = "Already available"
            #return status
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            print("Exception occured at user registration")
            return redirect(url_for('index'))
        finally:
            dbClose()
    return render_template('register.html')


@app.route('/login',methods=['POST','GET'])
def login():
    msg = ''
    if request.method == "POST":
        session.pop('user',None)
        mailid = request.form.get("email")
        password = request.form.get("pass1")
        #print(mobno+password)
        con = dbConnection()
        cursor = con.cursor()
        result_count = cursor.execute('SELECT * FROM userdetailes WHERE email = %s AND password = %s', (mailid, password))
        #a= 'SELECT * FROM userdetails WHERE mobile ='+mobno+'  AND password = '+ password
        print(result_count)
        #result_count=cursor.execute(a)
        # result = cursor.fetchone()
        if result_count>0:
            print(result_count)
            session['user'] = mailid
            return redirect(url_for('home'))
        else:
            print(result_count)
            msg = 'Incorrect username/password!'
            return msg
    return render_template('login.html')


@app.route('/Service')
def Service():
    return render_template('Service.html')

@app.route('/adminlogin')
def adminlogin():
    return render_template('adminlogin.html')

@app.route('/admindash',methods=['POST','GET'])
def admindash():
    con = dbConnection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM userdetailes")
    result1 = cursor.fetchall()
    
    print(result1)
    
    return render_template('admindash.html',result1=result1)

@app.route('/logout')
def logout():

    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        # Get the form data
        Id = request.form['id']
        username = request.form['username']
        address = request.form['address']
        contact = request.form['contact']
        email = request.form['email']
        password = request.form['password']
        
        # Connect to the database
        con = dbConnection()
        cursor = con.cursor()
        
        # Update the user information in the database
        update_query = "UPDATE userdetailes SET name=%s, address=%s, phone=%s, email=%s, password=%s WHERE Id=%s"
        cursor.execute(update_query, (username, address, contact, email, password, Id))
        
        # Commit the changes
        con.commit()
        
        # Close the cursor and database connection
        cursor.close()
        con.close()
        
        return redirect(url_for('admindash'))
        
@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    con = dbConnection()
    cursor = con.cursor()
    delete_query = "DELETE FROM userdetailes WHERE Id = %s"
    cursor.execute(delete_query, (user_id,))
    con.commit()
    cursor.close()
    con.close()

    return "User deleted successfully"


if __name__=="__main__":
    app.run("0.0.0.0")
    # app.run(debug=True)