import xml.etree.ElementTree as ET
import os
import nltk
import re
import configparser
import csv
import logging
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_config = os.path.join(diretorio_atual, '../cfg/INDEX.CFG')
caminho_log = os.path.join(diretorio_atual, '../logs/indexador.log')

logging.basicConfig(filename=caminho_log, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')

logging.info('Lendo arquivo .CFG')
configs = configparser.RawConfigParser()
configs.read(caminho_config)
fonte_lista = configs.get('INDEX.CFG', 'LEIA')

caminho_lista = os.path.join(diretorio_atual, '../outputs/' + fonte_lista)

dict = {}
id_artigos = []

with open(caminho_lista, ) as input_csv:
    leitor_csv = csv.reader(input_csv, delimiter= ';')
    for row in leitor_csv:
        if len(row[0]) >= 2 and not bool(re.search(r'[\d!@#$%^&*()_+{}|:"<>?`\-=[\];\',.\\/]', row[0])):
            dict[row[0]] = eval(row[1])
            for id in eval(row[1]):
                id_artigos.append(id)
input_csv.close()

id_artigos = sorted(set(id_artigos))