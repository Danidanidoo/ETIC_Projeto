#Linha de codigo dedicada a realizar a ligação entre os comandos do script "default.py" e a variavel "app" do script "__init__.py" da pasta principal "Projeto"
from Projeto import app
from flask import Flask, render_template, request
lg_done = False
try:
    file = open('Login.txt','r+')
except IOError:
    file = open('Login.txt','w+')

Login_DB = file.readlines()

file.close()


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
                    #Se Palavras[0] (Username), corresponder a algum User da base de dados, então...
                    if Palavras[cont] == request.form['Cliente_User']:
                        #Contador +1
                        cont += 1
                        #Se Palavras[1], corresponder a alguma Pass da base de dados, então...
                        if Palavras[cont] == request.form['Cliente_Pass']:
                            #Faz isto
                            #global lg_done = True
                            return render_template("index.html", Cliente_Pass='Funcionou', Cliente_User='Great Job!')
                        #Se Palavras[0](User), for encontrado mas Palavras[1](Pass) não for encontrado na Base de Dados, então...
                        else:
                            #Faz isto:
                            return render_template("login.html", Pass_Errada='A Password Introduzida está incorreta!')
                    #Se Palavras[0] (Username), não for encontrado na Base de Dados, então...
                    else:
                        cont += 1
                        #Se Palavras[1] for encontrado:
                        if Palavras[cont] == request.form['Cliente_Pass']:
                            return render_template("login.html", User_Errado='O seu Username não está correto!')
                        else:
                            return render_template("login.html", User_Errado='O seu Username não está correto!')
    
    #Caso o utilizador digite "endereço/login" sem antes ter passado pela rota principal "/home", então ele será redirecionado para a tela de Login
    return render_template("login.html")