import os
import subprocess

def altera_cfg(stemmer, nome):
    cfg_path = os.path.join(diretorio_atual, "..", "cfg", nome)
    with open(cfg_path, 'r') as file:
        linhas = file.readlines()
    if "STEMMER" not in linhas[-1]:
        linhas.append(f"STEMMER= {stemmer}\n")
    else:
        linhas[-1] = f"STEMMER= {stemmer}\n"
    with open(cfg_path, 'w') as file:
        file.writelines(linhas)

diretorio_atual = os.path.dirname(os.path.abspath(__file__))

while True:    
    selecao = input('Insira 1 para o uso de Stemmer e 0 se não desejar: ')
    if selecao == '1' or selecao == '0':
        break
    print("Valor inválido, insira novamente")

if selecao == '1':
    stemmer = True
else: 
    stemmer = False

altera_cfg(stemmer, 'GLI.CFG')
altera_cfg(stemmer, 'PC.CFG')

modulos = [
    os.path.join(diretorio_atual, "Lista_invertida.py"),
    os.path.join(diretorio_atual, "Processador.py"),
    os.path.join(diretorio_atual, "Indexador.py"),
    os.path.join(diretorio_atual, "buscador.py")
]

for modulo in modulos:
    subprocess.run(["python", modulo])