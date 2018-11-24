#biblioteca de funcoes auxiliares contendo todas as outras bibliotecas. Ver codigo para mais detalhes
import aux_lib
from db import DB

import sys

sys.setrecursionlimit(15000)

##Prefixo do local das tabelas fonte para a extração de dados
prefix_loc = "tabelas_mcti\\formatada\\2"

#Trie de testes
teste = aux_lib.generate_table_trie(prefix_loc)

db_teste = DB(teste)

#s = aux_lib.suffix_search(db_teste.key_cols,'ano')


