try:
    file = open('Login.txt','r+')
except IOError:
    file = open('Login.txt','w+')

Login_DB = file.readlines()
'''
print (Login_DB)
for linha in Login_DB:
    print(linha)
    Palavras = linha.split("|")
    print (Palavras)
input()
'''