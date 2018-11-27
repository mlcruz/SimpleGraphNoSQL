#biblioteca de funcoes auxiliares contendo todas as outras bibliotecas. Ver codigo para mais detalhes
import aux_lib
from db import DB
import menus
from menus import Container

#Curses para interface grafica
import curses


import sys

sys.setrecursionlimit(15000)

##Prefixo do local das tabelas fonte para a extração de dados
prefix_loc = r"C:\Users\PC\source\repos\Trabalho_final_cpd\SimpleGraphNoSQL\fast"

#Trie de testes
teste = aux_lib.generate_table_trie(prefix_loc)

db_teste = DB(teste)

#aux_lib.save_trie(db_teste.key_cols,'key_col')

#################INICIALIZA REPL###################

t = db_teste.tables.strings_dict[db_teste.tables.strings_list[0]]
l = t.table_data[6][0].child_nodes
