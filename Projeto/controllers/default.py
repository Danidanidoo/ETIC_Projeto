#Linha de codigo dedicada a realizar a ligação entre os comandos do script "default.py" e a variavel "app" do script "__init__.py" da pasta principal "Projeto"
from Projeto import app
from flask import Flask, render_template, request
lg_done = False

@app.route("/")
@app.route("/home")
@app.route("/Home")
@app.route("/HOME")
@app.route("/Index")
@app.route("/INDEX")
@app.route("/index")
def index():
    if lg_done == False:
        return render_template("login.html")
    else:
        return render_template("index.html")
    
@app.route("/login", methods=['GET', 'POST'])
@app.route("/Login", methods=['GET', 'POST'])
@app.route("/LOGIN", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['BT_LOG'] == 'SIGNIN':
            return render_template("signIn.html")
        
        if request.form['BT_LOG'] == 'LOGIN':
            Cliente_User = request.form['Cliente_User']
            Cliente_Pass = request.form['Cliente_Pass']
            return render_template("index.html", Cliente_Pass=Cliente_Pass, Cliente_User=Cliente_User)