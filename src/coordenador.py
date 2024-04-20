import os
import subprocess

diretorio_atual = os.path.dirname(os.path.abspath(__file__))

modulos = [
    os.path.join(diretorio_atual, "Lista_invertida.py"),
    os.path.join(diretorio_atual, "Processador.py"),
    os.path.join(diretorio_atual, "Indexador.py"),
    os.path.join(diretorio_atual, "buscador.py")
]

for modulo in modulos:
    subprocess.run(["python", modulo])