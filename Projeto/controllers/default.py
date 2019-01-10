#Linha de codigo dedicada a realizar a ligação entre os comandos do script "default.py" e a variavel "app" do script "__init__.py" da pasta principal "Projeto"
from Projeto import app
from Projeto.models import Login_DB
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
            if request.form['Cliente_User'] == "Admin":
                if request.form['Cliente_Pass'] == "Admin":
                    return render_template("index.html", Cliente_Pass=request.form['Cliente_User'], Cliente_User=request.form['Cliente_Pass'])
            
            else:
                for linha in Login_DB:
                    Palavras = linha.split("|")
                    cont = 0
                    #for palavra in Palavras:
                    if Palavras[cont] == "Daniel":
                        cont += 1
                        if Palavras[cont] == "y6BE$1aY3NWK":
                            return render_template("index.html", Cliente_Pass='Funcionou', Cliente_User='Great Job!')
                        else:
                            return render_template("index.html", Cliente_Pass='Cliente_Pass', Cliente_User='Cliente_User')

                            
            #Cliente_User = 
            #Cliente_Pass = 
            #