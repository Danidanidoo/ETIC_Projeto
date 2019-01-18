#Linha de codigo dedicada a realizar a ligação entre os comandos do script "default.py" e a variavel "app" do script "__init__.py" da pasta principal "Projeto"
import re
import random
from Projeto import app
from flask import Flask, render_template, request, Markup, flash
import math
lg_done = False


def calc_distancia(X1, Y1, X2, Y2):
    rad=math.pi/180
    dX=X2-X1
    dY=Y2-Y1
    R=6372.795477598
    a=(math.sin(rad*dX/2))**2 + math.cos(rad*X1)*math.cos(rad*X2)*(math.sin(rad*dY/2))**2
    distancia=2*R*math.asin(math.sqrt(a))
    return distancia

def load_login():
    try:
        file = open('Login.txt','r+')
    except IOError:
        file = open('Login.txt','w+')
    Login_DB = file.readlines()
    file.close()
    return Login_DB

def load_cliente_DB():
    try:
        file = open('Cliente.txt','r+')
    except IOError:
        file = open('Cliente.txt','w+')
    Cliente_DB = file.readlines()
    file.close()
    return Cliente_DB

def load_veiculos():
    try:
        file = open('Viatura.txt','r+')
    except IOError:
        file = open('Viatura.txt','w+')
                
    Viatura_DB = file.readlines()
    file.close()
    cont = 1
    script = ''
    for linha in Viatura_DB:
        Palavras = linha.split("|")
        if cont == 1:
            script = script + '<tr>'
        while cont <= 9:
            script = script +'<td>'+Palavras[cont]+'</td>'
            if cont == 9:
                script = script +'</tr>'
            cont += 1
        else:
            cont = 1
    return script

def load_cliente():
    try:
        file = open('Cliente.txt','r+')
    except IOError:
        file = open('Cliente.txt','w+')
                
    Cliente_DB = file.readlines()
    file.close()
    cont = 1
    script = ''
    for linha in Cliente_DB:
        Palavras = linha.split("|")
        if cont == 1:
            script = script + '<tr>'
        while cont <= 2:
            script = script +'<td>'+Palavras[cont]+'</td>'
            if cont == 2:
                script = script +'</tr>'
            cont += 1
        else:
            cont = 1
    return script

def load_tabela():
    message = Markup(load_veiculos())
    flash(message, category='veiculo')

def load_tabela_cliente():
    message = Markup(load_cliente())
    flash(message, category='cliente')

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
        if request.form['BT_LOG'] == 'SIGNUP':
            return render_template("signup.html")
        
        if request.form['BT_LOG'] == 'LOGIN':
            if request.form['Cliente_User'] == "Admin":
                if request.form['Cliente_Pass'] == "Admin":
                    load_tabela()
                    load_tabela_cliente()
                    return render_template("Admin.html", Cliente_User=request.form['Cliente_Pass'])
            
            else:
                for linha in load_login():
                
                    Palavras = linha.split("|")
                    cont = 2
                    #Se Palavras[2] (Username), corresponder a algum User da base de dados, então...
                    if Palavras[cont] == request.form['Cliente_User']:
                        #Contador +1
                        cont += 1
                        #Se Palavras[3], corresponder a alguma Pass da base de dados, então...
                        if Palavras[cont] == request.form['Cliente_Pass']:
                            #Faz isto
                            #global lg_done = True
                            return render_template("Cliente.html", Cliente_Pass='Funcionou', Cliente_User='Great Job!')
                        #Se Palavras[2](User), for encontrado mas Palavras[3](Pass) não for encontrado na Base de Dados, então...
                        else:
                            #Faz isto:
                            return render_template("login.html", Pass_Errada='A Password Introduzida está incorreta!')
                for linha in load_login():
                    Palavras = linha.split("|")
                    cont = 2
                    #Se Palavras[2] (Username), não for encontrado na Base de Dados, então...
                    cont += 1
                    #Se Palavras[3] for encontrado:
                    if Palavras[cont] == request.form['Cliente_Pass']:
                       return render_template("login.html", User_Errado='O seu Username não está correto!')
                    else:
                        return render_template("login.html", User_Errado='O seu Username não está correto!')
    
    #Caso o utilizador digite "endereço/login" sem antes ter passado pela rota principal "/home", então ele será redirecionado para a tela de Login
    return render_template("login.html")

@app.route("/signup", methods=['GET', 'POST'])
@app.route("/SIGNUP", methods=['GET', 'POST'])
@app.route("/Signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if request.form['BT_SIGNUP'] == 'SIGNUP':
            for linha in load_login():

                Palavras = linha.split("|")
                #Se Palavras[2] (Username), corresponder a algum User da base de dados, então...
                if Palavras[2] == request.form['Cliente_User']:
                    return render_template("signup.html", User_Existe='O Username introduzido já existe')

            if request.form['Cliente_Pass1'] != request.form['Cliente_Pass2']:
                return render_template("signup.html", Pass_Erro='As Password não correspondem')
    
            if re.match(r'^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$', request.form['Cliente_Pass1']):
                for linha in load_login():
                    Palavras = linha.split("|")
                    ultimo_ID = Palavras[1]

                file = open('Login.txt','a')
                file.write('|'+str((int(ultimo_ID)+1))+'|'+request.form['Cliente_User']+'|'+request.form['Cliente_Pass1']+'|'+'\n')
                file.close()

                for linha in load_cliente_DB():
                    Palavras = linha.split("|")
                    ultimo_ID = Palavras[1]

                file = open('Cliente.txt','a')
                file.write('|'+str((int(ultimo_ID)+1))+'|'+request.form['Cliente_Nome']+'|'+'\n')
                file.close()
                return render_template("Conta_Criada.html")
            else:
                return render_template("signup.html", Pass_Erro='A Password deve ter pelo menos 6 caracteres, pelo menos uma maiuscula, um algarismo e conter pelo menos um caracter especial')


@app.route("/Conta_Criada", methods=['GET', 'POST'])
def Conta_Criada():
    if request.method == 'POST':
        if request.form['BT_SIGNUP'] == 'SIGNUP':
            return render_template('login.html')




@app.route("/Admin", methods=['GET', 'POST'])
def Admin():
    

    if request.method == 'POST':
        if request.form['BT_VEICULO'] == 'ADICIONAR':
            return render_template('Add_Veiculo.html')
        
        elif request.form['BT_VEICULO'] == 'REMOVER':
            return render_template('Del_Veiculo.html')


@app.route("/Add_Veiculo", methods=['GET', 'POST'])
def Add_Veiculo():
    if request.method == 'POST':
        if request.form['BT_VEICULO'] == 'ADICIONAR':
            try:
                file = open('Viatura.txt','r+')
            except IOError:
                file = open('Viatura.txt','w+')
                
            Viatura_DB = file.readlines()

            for linha in Viatura_DB:

                Palavras = linha.split("|")
                
                ultimo_ID = Palavras[1]


            file = open('Viatura.txt','a')
            file.write('|'+str((int(ultimo_ID)+1))+'|'+request.form['Marca']+'|'+request.form['Matricula']+'|'+request.form['Condutor']+'|'+request.form['KM']+'|'+request.form['Valor Faturado (€)']+'|'+request.form['Servicos']+'|'+'Ativo'+'|'+request.form['Tipo']+'|'+'2.5'+'|'+'2.5'+'|'+'\n')
            file.close()
            load_tabela()
            load_tabela_cliente()
            return render_template('Admin.html')
       
        elif request.form['BT_VEICULO'] == 'CANCELAR':
            load_tabela()
            load_tabela_cliente()
            return render_template('Admin.html')

@app.route("/Del_Veiculo", methods=['GET', 'POST'])
def Del_Veiculo():
    if request.method == 'POST':
        if request.form['BT_VEICULO'] == 'CANCELAR':
            load_tabela()
            load_tabela_cliente()
            return render_template('Admin.html')
        elif request.form['BT_VEICULO'] == 'REMOVER':

            try:
                file = open('Viatura.txt','r+')
            except IOError:
                file = open('Viatura.txt','w+')
                
            Viatura_DB = file.readlines()
            file.close()
            for linha in Viatura_DB:

                Palavras = linha.split("|")
                if Palavras[1] == request.form['ID']:
                    Palavras.pop(8)
                    Palavras.insert(8,"Inativo")
                    nova_linha = '|'.join(Palavras)
            Viatura_DB.pop(int(request.form['ID'])-1)
            Viatura_DB.insert(int(request.form['ID'])-1, nova_linha)

            file = open('Viatura.txt','w')
            for linha in Viatura_DB:
                file.write(str(linha))
            file.close()
            load_tabela()
            load_tabela_cliente()
            return render_template('Admin.html')

@app.route("/Cliente", methods=['GET', 'POST'])
def Cliente():
    
    try:
        file = open('Viatura.txt','r+')
    except IOError:
        file = open('Viatura.txt','w+')
                
    Viatura_DB = file.readlines()
    file.close()
    cont = 0
    nova_linha = Viatura_DB
    if request.method == 'POST':
        if request.form['BT_CLIENTE'] == 'PESQUISA':
            Distancia_a = 1.1
            Distancia_ab = calc_distancia(float(request.form['Cliente_X']), float(request.form['Cliente_Y']), float(request.form['Destino_X']), float(request.form['Destino_Y']))
            for linha in Viatura_DB:
                Palavras = linha.split("|")
                if Palavras[9] == 'carro':
                    custo = 3 + (Distancia_ab * 0.40)
                    tempo_ab = Distancia_ab / 30
                    tempo_a = Distancia_a / 30
                    Veiculo_X = Palavras[10]
                    Veiculo_Y = Palavras[11]
                    Distancia_a = calc_distancia(float(request.form['Cliente_X']), float(request.form['Cliente_Y']), float(Veiculo_X), float(Veiculo_Y))
                else:
                    custo = 4 + (Distancia_ab * 0.70)
                    tempo_ab = Distancia_ab / 25
                    tempo_a = Distancia_a / 25
                    Distancia_a = calc_distancia(float(request.form['Cliente_X']), float(request.form['Cliente_Y']), float(Veiculo_X), float(Veiculo_Y))
                nova_linha[cont] ='|'+ Palavras[2] + '|' + Palavras[4] + '|' + str(int(Distancia_a)) + '|'+str(int(custo))+'|'+str(int(tempo_ab))+'|'+str(int(tempo_a))+'|'+Palavras[9]+'|'+'\n'
                cont += 1
            
            script = ''
            
            
            cont = 1
            for linha in nova_linha:
                Palavras = linha.split("|")
                if cont == 1:
                    script = script + '<tr>'
                while cont <= 7:
                    script = script +'<td>'+Palavras[cont]+'</td>'
                    if cont == 7:
                        script = script +'</tr>'
                    cont += 1
                else:
                    cont = 1
                        
            
            message = Markup(script)
            flash(message, category='veiculo_cliente')
            return render_template('Cliente.html')