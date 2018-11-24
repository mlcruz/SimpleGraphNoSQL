#biblioteca de funcoes auxiliares contendo todas as outras bibliotecas. Ver codigo para mais detalhes
import aux_lib
import re
import sys

sys.setrecursionlimit(15000)



##Prefixo do local das tabelas fonte para a extração de dados
prefix_loc = "tabelas_mcti\\formatada\\2"


teste = aux_lib.generate_db_trie(prefix_loc)


#aux_lib.save_trie(teste,'teste.obj')
#retorno = aux_lib.load_trie('teste.obj')

p = aux_lib.prefix_search(teste,"brasil")
s = aux_lib.suffix_search(teste,"atividade")
r = aux_lib.regex_search(teste,r'atividade')







