import xml.etree.ElementTree as ET
import os
import nltk
import re
import configparser
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')
stop_words = set([x.upper() for x in stopwords.words('english')])

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_config = os.path.join(diretorio_atual, '../cfg/GLI.CFG')

configs = configparser.RawConfigParser()
configs.read(caminho_config)

output = configs.get('GLI.CFG', 'ESCREVA')
arquivos = [os.path.join(diretorio_atual, '../data/' + x) for x in configs.get('GLI.CFG', 'LEIA').split(",")]

abstracts = []
extracts = []

for caminho_arquivo in arquivos:
    tree = ET.parse(caminho_arquivo)
    root = tree.getroot()
    for artigo in root.findall('RECORD'):
        
        abstract = artigo.find('ABSTRACT')
        extract = artigo.find('EXTRACT')
        
        if abstract is not None and len(abstract.text) > 0:
            abstract_limpo = re.sub(r'[\'\'``,$&#=+@.%;(){}\[\]]', '', abstract.text)
            abstract_tokens = [p.upper() for p in word_tokenize(abstract_limpo)]
            abstract_palavras = [p for p in abstract_tokens if not p in stop_words]
            abstracts.append((artigo.find('RECORDNUM').text, abstract_palavras))
        
        elif extract is not None and len(extract.text) > 0:
            extract_limpo = re.sub(r'[\'\'``,$&#=+@.%;(){}\[\]]', '', extract.text)
            extract_tokens = [p.upper() for p in word_tokenize(extract_limpo)]
            extract_palavras = [p for p in extract_tokens if not p in stop_words]
            extracts.append((artigo.find('RECORDNUM').text, extract_palavras))

for desc in extracts:
    print(desc)
