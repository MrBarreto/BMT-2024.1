import xml.etree.ElementTree as ET
import os
import nltk
import re
import configparser
import csv
import logging
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_config = os.path.join(diretorio_atual, '../cfg/PC.CFG')
caminho_log = os.path.join(diretorio_atual, '../logs/PC.log')

logging.basicConfig(filename=caminho_log, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')

logging.info('Lendo arquivo .CFG')
configs = configparser.RawConfigParser()
configs.read(caminho_config)
fonte_consultas = configs.get('PC.CFG', 'LEIA')
output_consultas = configs.get('PC.CFG', 'CONSULTAS')
output_esperados = configs.get('PC.CFG', 'ESPERADOS')

logging.info('Iniciando download de pacotes do NLTK')
nltk.download('punkt')
nltk.download('stopwords')

logging.info('Processando Stopwords')
stop_words = set([x.upper() for x in stopwords.words('english')])

arquivo_consultas = os.path.join(diretorio_atual, '../data/' + fonte_consultas)
arquivo_query = os.path.join(diretorio_atual, '../outputs/' + output_consultas)
arquivo_esperados = os.path.join(diretorio_atual, '../outputs/' + output_esperados)

logging.info('Iniciando o parse do arquivo %s', arquivo_consultas)
tree = ET.parse(arquivo_consultas)
root = tree.getroot()

with open(arquivo_query, mode='w', newline='') as consultas_file:
    consultas_writer = csv.writer(consultas_file, delimiter=';')
    consultas_writer.writerow(['QueryNumber', 'QueryText'])
    for query in root.findall('./QUERY'):
        
        query_number = query.find('QueryNumber').text
        query_text = query.find('QueryText').text.strip()
        
        logging.info('Iniciando o processamento da consulta número %s', query_number)
        
        query_limpa = re.sub(r'[\'"`:,$&#=+@.%;(){}\[\]]', '', query_text)
        query_tokens = [p.upper() for p in word_tokenize(query_limpa)]
        query_palavras = [p for p in query_tokens if not p in stop_words]
        
        consultas_writer.writerow([query_number, query_palavras])
        logging.info('Terminando o processamento da consulta número %s', query_number)

with open(arquivo_esperados, mode='w', newline='') as esperados_file:
    esperados_writer = csv.writer(esperados_file, delimiter=';')
    esperados_writer.writerow(['QueryNumber', 'DocNumber', 'DocVotes'])
    
    for query in root.findall('./QUERY'):
        query_number = query.find('QueryNumber').text
        logging.info('Iniciando o processamento dos resultados esperados consulta número %s', query_number)
        for record in query.find('Records').findall('Item'):
            artic_number = record.text
            vote = record.get('score')
            esperados_writer.writerow([query_number, artic_number, vote])
        logging.info('Terminando o processamento dos resultados esperados consulta número %s', query_number)