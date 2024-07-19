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
    for documento in range(len(modelo[0])):
        similaridade = -1
        coluna = modelo[:,documento]
        similaridade = np.dot(vetor, coluna)/(norma_vetor*norma_matriz[documento])
        similaridades.append(similaridade)
    return similaridades

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_config = os.path.join(diretorio_atual, '../cfg/BUSCA.CFG')
caminho_log = os.path.join(diretorio_atual, '../logs/BUSCA.log')

logging.basicConfig(filename=caminho_log, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')

logging.info('Lendo arquivo .CFG')
configs = configparser.RawConfigParser()
configs.read(caminho_config)
stemmer_string = configs.get('BUSCA.CFG', 'STEMMER')
stemmer = stemmer_string == 'True'
modelo, metadados = [os.path.join(diretorio_atual, '../outputs/' + x) for x in configs.get('BUSCA.CFG', 'MODELO').split(",")]
dados_consultas = os.path.join(diretorio_atual, '../outputs/' + configs.get('BUSCA.CFG', 'CONSULTAS'))
if stemmer:
    output_resultados = os.path.join(diretorio_atual, '../outputs/' + configs.get('BUSCA.CFG', 'RESULTADOS') + 'Stemmer.csv')
else:
    output_resultados = os.path.join(diretorio_atual, '../outputs/' + configs.get('BUSCA.CFG', 'RESULTADOS') + 'NoStemmer.csv')

logging.info('Extraindo metadados do modelo vetorial')
with open(metadados, 'r') as file:
    compact_json = file.read()

combined_dict = json.loads(compact_json)

logging.info('Separando metadados e extraindo o modelo')
palavras = combined_dict["palavras"]
artigos = combined_dict["artigos"]
artigos_inv = combined_dict["artigos_inv"]
modelo = np.loadtxt(modelo, dtype=float)
num_palavras = len(modelo)

consultas_dict = {}

logging.info('Iniciando o carregamento das consultas preprocessadas')
with open(dados_consultas, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        numero_consulta = int(row['QueryNumber'])
        texto_consulta = eval(row['QueryText'])  
        consultas_dict[numero_consulta] = texto_consulta
logging.info('Terminando o carregamento das consultas preprocessadas')

consultas_vec = {}

logging.info('Iniciando a transformação das consultas em vetores')
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
logging.info('Terminando a transformação das consultas em vetores')

logging.info('Calculando a norma de cada documento')
norma_colunas = np.linalg.norm(modelo, axis=0)
logging.info('Norma calculada')

dic_resultados = {}

logging.info('Iniciando o calculo das similaridades')
for id, vetor in consultas_vec.items():
    pesos = similaridades(modelo, vetor, norma_colunas)
    pesos_mapeados = [[artigos_inv[str(indice)], pesos[indice]] for indice in range(len(pesos))]
    pesos_mapeados.sort(key=lambda x: x[1], reverse = True)
    vetor_resultado = [[indice + 1, pesos_mapeados[indice][0], pesos_mapeados[indice][1]] for indice in range(len(pesos_mapeados))]
    dic_resultados[id] = vetor_resultado
logging.info('Terminando o calculo das similaridades')

logging.info('Escrevendo CSV de resultados')
with open(output_resultados, mode='w', newline='') as resultados_file:
    resultados_writer = csv.writer(resultados_file, delimiter=';')
    resultados_writer.writerow(['QueryNumber', 'List'])
    for id, vetores in dic_resultados.items():
        for vetor in vetores:
            resultados_writer.writerow([id, vetor])
logging.info('CSV de resultados escrito')
