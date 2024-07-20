# BMT-2024.1
Repositório da Disciplina de Busca e Mineração de texto, período 2024.1

## Estrutura
O código em si está contido na pasta /src, com os módulos:
### Módulos
 - `Lista_invertida.py`: Gera lista invertida
 - `Processador.py`: Pocessa arquivo de consultas
 - `Indexador.py:`: Cria as matrizes de tf-idf a partir da lista invertida
 - `buscador.py`: Cria vetores de consulta e calcula as similariades de cada consulta baseada na matriz anterior do tf-idf.
 - `coordenador.py`: Executa todos os módulos na sequência correta e ajusta os parâmetros de stemmer.
 - `metrica.ipynb`: Calcula as métricas dos resultados obtidos.

Temos também algumas pastas anexas:

### Pastas:
- `avalia`: Contém os resultados das métricas.
- `cfg`: Contém os arquivos de configuração necessários para o funcionamento dos módulos.
- `data` Contém os arquivos com  os artigos a serem indexados e as consultas
- `logs`: Logs de execução de cada módulo
- `outputs`: Saída dos módulos.
- `outputs_stemmer` e `outputs_nostemmer`: Separadas manualmente, a partir delas são calculadas as métricas.

