from flask import Flask, jsonify, request, render_template
import json
from databaseHandler import getItems, signUp, login, check_token, getUserItems, updateItems
from flask_cors import CORS
import sqlite3
from passlib.hash import bcrypt
import jwt, datetime, json
app = Flask(__name__)
CORS(app)

@app.route('/items', methods=['GET'])
def get_items():
    list = getItems()
    return jsonify(list)

@app.route('/useritems', methods=['GET'])
def get_useritems():
    token = request.headers.get('Authorization')
    if token:
        token = token.replace('Bearer ', '')
        user_id = check_token(token)
        list = getItems()
        if user_id:
            return jsonify(getUserItems(user_id),list,user_id)
        
@app.route('/updateitems', methods=["POST","OPTIONS"])
def update_useritems():
    if request.method =="POST":
        items = request.get_json()
        token = request.headers.get('Authorization')
        if True:
            token = token.replace('Bearer ', '')
            user_id = check_token(token)
            # print(user_id)
            if user_id:
                updateItems(user_id,json.dumps(items))
                return jsonify("ok")
            
            
    elif request.method == "OPTIONS":
        return jsonify("Ok")

            
            
            
            

@app.route("/signup",methods=["GET","POST","OPTIONS"])
def clientSignup():
    if request.method == "POST":
     #   try:
        uname = request.get_json()["uname"]
        pwd = request.get_json()["psw"]
        signUp(uname,pwd)
        return jsonify("ok")
        # except:
        #     return jsonify("error")
    elif request.method =="GET":
        return render_template("signup.html")
    elif request.method == "OPTIONS":
        return jsonify("Ok")
    
@app.route("/login",methods=["GET","POST","OPTIONS"])
def test():
    if request.method == "POST":
     #   try:
        uname = request.get_json()["uname"]
        pwd = request.get_json()["psw"]
        token = login(uname,pwd)
        if token != "Invalid credentials":
            print(token)
            response = jsonify(token=token)
            response.status_code = 200
            return response
        else:
            response = jsonify(message='Invalid credentials')
            response.status_code = 401
            return response
    elif request.method =="GET":
        return render_template("login.html")
    elif request.method == "OPTIONS":
        return jsonify("Ok")
    
@app.route("/",methods=["GET"])
def redirect():
    return render_template("test.html")    

@app.route("/index",methods=["GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")   
    
if __name__ == '__main__':
    app.run()