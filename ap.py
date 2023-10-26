from flask import Flask, render_template, request, redirect, url_for,session
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

app.secret_key="abi1234"

client = MongoClient('mongodb://localhost:27017')
db = client.db
doc = db.doc

def isloggedin():
    return "username" in session


@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        username=request.form['name']
        password=request.form['pass']
        login=db.signup.find_one({'username': username, 'pass': password})
        if login:
            session['username']=username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid Credentials"
    return render_template("login.html")

@app.route('/signup',methods=["GET","POST"])
def signup():
    if request.method == 'POST':
        signup = {
            'username': request.form['name'],
            'gender':request.form['gender'],
            'phone':request.form['phone'],
            'email':request.form['email'],
            'pass':request.form['pass']
        }
        db.signup.insert_one(signup)
        return redirect(url_for('login'))
    return render_template("signup.html")

@app.route('/patients')
def manage_patients():
        patients = db.patients.find()  # Retrieve patients from MongoDB
        return render_template('index.html', patients=patients)

# Add more routes for doctors, appointments, etc.
@app.route('/add_patient', methods=['POST'])
def add_patient():
    if request.method == 'POST':
        patient_data = {
            'name': request.form['name'],
            'age': request.form['age'],
            'gender':request.form['gender'],
            'phone':request.form['phone'],
            'time':request.form['time'],
            'date':request.form['date']
        }
        db.patients.insert_one(patient_data)
        return redirect(url_for('manage_patients'))
    
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_data(id):
    id_1=ObjectId(id)
    print(id_1)
    data = db.patients.find_one({"_id": id_1})
    if request.method == 'POST':
        updated_data = {
            "name": request.form['name'],
            "age": int(request.form['age']),
            'gender':request.form['gender'],
            'phone':request.form['phone'],
            'time':request.form['time'],
            'date':request.form['date']
        }
        db.patients.update_one({"_id": id_1}, {"$set": updated_data})
        return redirect(url_for('manage_patients'))
    return render_template('edit.html', data=data)

@app.route('/delete/<id>', methods=["GET",'POST'])
def delete_data(id):
    db.patients.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('manage_patients'))

@app.route('/logout')
def logout():
    session.pop("username",None)
    return redirect (url_for("login"))
    



if __name__ == "__main__":
    app.run(debug=True,port=8000)