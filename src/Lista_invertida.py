import xml.etree.ElementTree as ET
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(diretorio_atual, '../data/cf74.xml')

tree = ET.parse(caminho_arquivo)
root = tree.getroot()
abstracts = []
extracts = []

for artigo in root.findall('RECORD'):
    abstract = artigo.find('ABSTRACT')
    extract = artigo.find('EXTRACT')
    if abstract is not None and len(abstract.text) > 0:
        abstracts.append((artigo.find('RECORDNUM').text, abstract.text.strip()))
    elif extract is not None and len(extract.text) > 0:
        extracts.append((artigo.find('RECORDNUM').text, extract.text.strip()))

for id, abstract in abstracts:
    print(f"Abstract {id}: {abstract}")
    print()

for id, extract in extracts:
    print(f"Extract {id}: {extract}")
    print()

