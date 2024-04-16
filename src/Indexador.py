import xml.etree.ElementTree as ET
import os
import nltk
import re
import configparser
import csv
import logging
import numpy as np
import math
import json

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_config = os.path.join(diretorio_atual, '../cfg/INDEX.CFG')
caminho_log = os.path.join(diretorio_atual, '../logs/indexador.log')

logging.basicConfig(filename=caminho_log, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')

logging.info('Lendo arquivo .CFG')
configs = configparser.RawConfigParser()
configs.read(caminho_config)
fonte_lista = configs.get('INDEX.CFG', 'LEIA')
output_vetor = configs.get('INDEX.CFG', 'ESCREVA')

caminho_lista = os.path.join(diretorio_atual, '../outputs/' + fonte_lista)

dict = {}
id_artigos = []

logging.info('Lendo arquivo com a lista invertida')
with open(caminho_lista, ) as input_csv:
    leitor_csv = csv.reader(input_csv, delimiter= ';')
    for row in leitor_csv:
        if len(row[0]) >= 2 and not bool(re.search(r'[\d!@#$%^&*()_+{}|:"<>?`\-=[\];\',.\\/]', row[0])):
            dict[row[0]] = eval(row[1])
            for id in eval(row[1]):
                id_artigos.append(id)
input_csv.close()

logging.info('Leitura da lista invertida terminada')

id_artigos = sorted(set(id_artigos))

dic_palavras = {}
dic_artigos ={}

col =  len(id_artigos)
lin = len(dict.keys())
palavras = list(dict.keys())

logging.info('Criando mapeamentos entre Palavras/Artigos e índices')
for i in range(col):
    dic_artigos[id_artigos[i]] = i

for i in range(lin):
    dic_palavras[palavras[i]] = i

vetorial  = np.zeros((lin, col), dtype= float)

for word, lista_artigos in dict.items():
    for artigo in lista_artigos:
        vetorial[dic_palavras[word]][dic_artigos[artigo]] = 1
"""
print(vetorial)
for linha in range(len(vetorial)):
    somatorio = 0
    for coluna in range(len(vetorial[0])):
        if vetorial[linha][coluna] == 1:
            elemento = dic_artigos_inv[coluna]
            if elemento in dict[dic_palavras_inv[linha]]:
                somatorio += 1
    if somatorio != len(set(dict[dic_palavras_inv[linha]])):
        print("fodeu")
"""
logging.info('Iniciando o processo de cálculo de peso das palavras nos artigos')
for linha in range(len(vetorial)):
    idf = 0
    for coluna in range(len(vetorial[0])):
        idf += vetorial[linha][coluna]
    idf = math.log10(len(vetorial[0])/idf)
    for coluna in range(len(vetorial[0])):
        vetorial[linha][coluna] = vetorial[linha][coluna]*idf

compact_dic ={"palavras": dic_palavras, "artigos":dic_artigos}

caminho_vetor = os.path.join(diretorio_atual, '../outputs/' + output_vetor)

caminho_metadados = os.path.join(diretorio_atual, '../outputs/metadados_indexador.txt')

compact_json = json.dumps(compact_dic)

logging.info('Salvando metadados no txt')
with open(caminho_metadados, 'w') as file:
    file.write(compact_json)
logging.info('Metadados salvos no txt')

logging.info('Savando a matriz')
np.savetxt(caminho_vetor, vetorial)
logging.info('Matriz Salva')