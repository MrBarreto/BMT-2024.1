import xml.etree.ElementTree as ET
import os
import configparser
import csv
import logging
import json
import numpy as np

def similaridades(modelo, vetor, norma_matriz):
    norma_vetor = np.linalg.norm(vetor)
    similaridades = []
    for documento in len(modelo[0]):
        similaridade = -1
        coluna = modelo[:,documento]
        similaridade = np.dot(vetor, coluna)/(norma_vetor*norma_matriz[coluna])
        similaridades.append(similaridade)
    return similaridades

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_config = os.path.join(diretorio_atual, '../cfg/BUSCA.CFG')
caminho_log = os.path.join(diretorio_atual, '../logs/BUSCA.log')

logging.basicConfig(filename=caminho_log, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')

logging.info('Lendo arquivo .CFG')
configs = configparser.RawConfigParser()
configs.read(caminho_config)
modelo, metadados = [os.path.join(diretorio_atual, '../outputs/' + x) for x in configs.get('BUSCA.CFG', 'MODELO').split(",")]
dados_consultas = os.path.join(diretorio_atual, '../outputs/' + configs.get('BUSCA.CFG', 'CONSULTAS'))
output_resultados = os.path.join(diretorio_atual, '../outputs/' + configs.get('BUSCA.CFG', 'RESULTADOS'))

with open(metadados, 'r') as file:
    compact_json = file.read()

combined_dict = json.loads(compact_json)

palavras = combined_dict["palavras"]
artigos = combined_dict["artigos"]
artigos_inv = combined_dict["artigos_inv"]
modelo = np.loadtxt(modelo, dtype=float)
num_palavras = len(modelo)

consultas_dict = {}

with open(dados_consultas, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        numero_consulta = int(row['QueryNumber'])
        texto_consulta = eval(row['QueryText'])  
        consultas_dict[numero_consulta] = texto_consulta

consultas_vec = {}

for id, tokens in consultas_dict.items():
    vetor  = np.zeros(num_palavras)
    for token in tokens:
        indice = -1
        try:
           indice = palavras[token]
        except:
            continue
        vetor[indice] = 1
    consultas_vec[id] = vetor

norma_colunas = np.linalg.norm(modelo, axis=0)












