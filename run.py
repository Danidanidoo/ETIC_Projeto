#Linha dedicada a importacao da variavel "app" do script "__init__.py" da pasta principal "Projeto"
from Projeto import app

#Se recebermos a pagina principal, o script executa a aplicacao
if __name__ == "__main__":
    app.run(debug=True)