from flask import Flask, request, jsonify, make_response
import os
import json
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import requests
import jwt
import datetime
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY']='TTMKryptoTask'
db = SQLAlchemy(app)

class Alert(db.Model):
    a_id=db.Column(db.Integer,primary_key=True, nullable=False)
    u_id=db.Column(db.String(80), nullable=False)
    a_target=db.Column(db.Integer,nullable=False)
    a_status=db.Column(db.String(20))

    def __repr__(self):
        return f"{self.a_id} - {self.a_target}"

class User(db.Model):
    u_id=db.Column(db.Integer,primary_key=True, nullable=False)
    u_secret=db.Column(db.String(25),nullable=False)
    u_email=db.Column(db.String(80),nullable=False)
    u_name=db.Column(db.String(80),nullable=False)

    def __repr__(self):
        return f"{self.u_id} - {self.u_secret} - {self.u_name} - {self.u_email}"

def token_required(f):
    @wraps(f)
    def decorated(args, **kwargs):
        if 'access_token' in request.headers:
            token = request.headers['access_token']
        if not token:
            return jsonify({'Response':'Token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(u_id=data['u_id']).first()
        except:
            return jsonify({'Response':'Invalid Token'})

        return f(current_user,args, **kwargs)
    return decorated


@app.route('/')
def index():
    response = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false')

    for coins in response.json():
        if(coins["symbol"]=="btc"):
            cp = str(coins["current_price"])
            return cp + ' is the price of $BTC right now!'

@app.route('/user',methods=['POST'])
def create_user():
    hashed_usecret = generate_password_hash(request.json["password"], method='sha256')
    db.session.add(User(u_secret=hashed_usecret, u_name=request.json["username"], u_email=request.json["email"]))
    db.session.commit()
    return {"Response":"New user created"}

@app.route('/login')
def user_login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response("Please enter username and password", 401, {"WWW-Authenticate":"Basic Realm='Login Failed'"})
    user_row = User.query.filter_by(u_name=auth.username).first()
    if not user_row:
        return make_response("Wrong username or password", 401, {"WWW-Authenticate":"Basic Realm='Login Failed'"})
    if check_password_hash(user_row.usecret, auth.password):
        token = jwt.encode({'u_id':User.u_id, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
        return jsonify({'token':token.decode(  'UTF-8')})

    return make_response("Wrong username or password", 401, {"WWW-Authenticate":"Basic Realm='Login Failed'"})

@app.route('/alerts',methods=['GET'])
@token_required
def view_alerts(current_user):
    qf=request.json["queryfilter"]
    if qf=='null':
        alerts = Alert.query.filter_by(u_id=request.json["u_id"]).all()
    else:
        alerts = Alert.query.filter_by(u_id=request.json["u_id"]).filter_by(a_status=qf).all()
    response=[]
    for a in alerts:
        response.append({'a_id':a.a_id, 'u_id':a.u_id, 'a_target':a.a_target, 'a_status':a.a_status})
    return {'Alerts':response}

@app.route('/alerts/create', methods=['POST'])
@token_required
def add_alert(current_user):
    newAlert = Alert(a_id=request.json['a_id'],u_id=request.json['u_id'],a_target=request.json['a_target'],a_status='Created')
    db.session.add(newAlert)
    db.session.commit()
    #return f"{'current_price': c_p,} and {'target_price': newAlert.a_target}"
    return {'your target':newAlert.a_target}

@app.route('/alerts/delete', methods=['PUT'])
@token_required
def remove_alert(current_user):
    r_aid=request.json["a_id"]
    row = Alert.query.filter_by(a_id=r_aid).first()
    row.a_status = "deleted"
    db.session.commit()
    return "Deleted Successfully"

def send_email(send_email_to,your_name):
    msg = MIMEMultipart()
    password = your_password
    msg['From'] = your_email
    msg['To']=send_email_to
    msg['Subject'] = "BTC Price has reached target. ACT Accordingly."

    message = "Dear client" + your_name + "\nBitcoin price has now crossed the target of: " + str(bitcoin_rate) + ". Time to Sell? \nRegards\nYour friendly neighborhoodly crypto alert API"
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'],msg['To'], message)
    server.quit()

    print("Alert has successfully been triggered, changing status now.")
your_name="ToTheMoon API"
your_email="tothemoon.api@gmail.com"
your_password="T0themoon.api"
#can use getpass for security i guess, hardcoding here for now
send_email_to="jessenth.ebenezer2019@vitstudent.ac.in"
alert_amount="23246"
bitcoin_rate=24504

@app.route('/emailmode')
def theInfiniteLoop():
    while True:
        url= "https://api.coindesk.com/v1/bpi/currentprice.json"
        response1 = requests.get(
            url,headers={"Accept":"application/json"},)
        data = response1.json()    
        bpi=data['bpi']
        USD=bpi['USD']
        bitcoin_rate=int(USD['rate_float'])
        targetList = Alert.query.filter(Alert.a_target <= bitcoin_rate).filter(Alert.a_status == 'created').all()
        for targetRow in targetList:
            userRow = User.query.filter_by(u_id=targetRow.u_id).first()
            send_email_to=userRow.u_email
            your_name=userRow.u_name
            send_email(send_email_to,your_name)
            targetRow.a_status = 'triggered'
            db.session.commit()
            print("Ctrl + C to quit, will check again in 5 minutes.")        
        
        print('Price is ' + str(bitcoin_rate) + '. Will check again in 5 minutes. Ctrl + C to exit.')
        time.sleep(300)
