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
caminho_config = os.path.join(diretorio_atual, '../cfg/GLI.CFG')
caminho_log = os.path.join(diretorio_atual, '../logs/GLI.log')

logging.basicConfig(filename=caminho_log, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')

logging.info('Iniciando download de pacotes do NLTK')
nltk.download('punkt')
nltk.download('stopwords')


stop_words = set([x.upper() for x in stopwords.words('english')])


logging.info('Lendo arquivo .CFG')
configs = configparser.RawConfigParser()
configs.read(caminho_config)

output = configs.get('GLI.CFG', 'ESCREVA')
caminho_output = os.path.join(diretorio_atual, '../outputs/' + output)
arquivos = [os.path.join(diretorio_atual, '../data/' + x) for x in configs.get('GLI.CFG', 'LEIA').split(",")]

abstracts = []
extracts = []
dict = {}

for caminho_arquivo in arquivos:
    
    logging.info('Iniciando o parse do arquivo %s', caminho_arquivo)
    tree = ET.parse(caminho_arquivo)
    root = tree.getroot()
    
    for artigo in root.findall('RECORD'):
        
        abstract = artigo.find('ABSTRACT')
        extract = artigo.find('EXTRACT')
        logging.info('Iniciando o processamento do Abstract do artigo número %s', artigo.find('RECORDNUM').text)
        
        if abstract is not None and len(abstract.text) > 0:
            abstract_limpo = re.sub(r'[\'"`:,$&#=+@.%;(){}\[\]]', '', abstract.text)
            abstract_tokens = [p.upper() for p in word_tokenize(abstract_limpo)]
            abstract_palavras = [p for p in abstract_tokens if not p in stop_words]
            abstracts.append((artigo.find('RECORDNUM').text, abstract_palavras))
        
        elif extract is not None and len(extract.text) > 0:
            extract_limpo = re.sub(r'[\'"`:,$&#=+@.%;(){}\[\]]', '', extract.text)
            extract_tokens = [p.upper() for p in word_tokenize(extract_limpo)]
            extract_palavras = [p for p in extract_tokens if not p in stop_words]
            extracts.append((artigo.find('RECORDNUM').text, extract_palavras))
        
        logging.info('Terminando o processamento do Abstract do arquivo %s', artigo.find('RECORDNUM').text)
    
    logging.info('Terminando processamento do artigo %s', caminho_arquivo)

logging.info('Iniciando a montagem do dicionário')
for tupla in abstracts:
    for palavras in tupla[1]:
        try:
            dict[palavras].append(int(tupla[0].strip()))
        except:
            dict[palavras] = [int(tupla[0].strip())]

for tupla in extracts:
    for palavras in tupla[1]:
        try:
            dict[palavras].append(int(tupla[0].strip()))
        except:
            dict[palavras] = [int(tupla[0].strip())]
logging.info('Terminando a montagem do dicionário')

logging.info('Adicionando dados ao CSV')
with open(caminho_output, 'w', newline='') as output_csv:
    escritor_csv = csv.writer(output_csv, delimiter=';')
    for palavra, lista in dict.items():
        escritor_csv.writerow([palavra] + [lista])
output_csv.close()
logging.info('CSV concluído')