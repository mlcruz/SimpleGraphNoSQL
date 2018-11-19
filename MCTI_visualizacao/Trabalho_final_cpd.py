#biblioteca de funcoes auxiliares
import aux_lib

from aux_lib import RawTable, Cell, get_cell, Table
from aux_lib import Trie, insert



file_pickle = open("pickle.obj",'wb')

##Prefixo do local das tabelas fonte para a extração de dados
prefix_loc = prefix_loc = "tabelas_mcti\\formatada\\2"


teste = aux_lib.generate_db_trie(prefix_loc)
aux_lib.save_trie(teste,'teste.obj')
retorno = aux_lib.load_trie('teste.obj')








