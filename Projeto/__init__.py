#Linha dedicada a importação da microframework "Flask"
from flask import Flask

#
app = Flask(__name__)
app.secret_key = 'Qualquercoisa'
#Linha dedidacada a importacao do script "default.py" da pasta "controllers"
from Projeto.controllers import default