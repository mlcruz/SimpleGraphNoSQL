#biblioteca de funcoes auxiliares contendo todas as outras bibliotecas. Ver codigo para mais detalhes
import aux_lib
from db import DB
import menus


#Curses para interface grafica
import curses


import sys

sys.setrecursionlimit(15000)

##Prefixo do local das tabelas fonte para a extração de dados
prefix_loc = "tabelas_mcti\\formatada\\2"

#Trie de testes
teste = aux_lib.generate_table_trie(prefix_loc)

db_teste = DB(teste)

#aux_lib.save_trie(db_teste.key_cols,'key_col')

#################INICIALIZA REPL###################

