#classe tabela representando um objeto tabela
from Tabela import Table, Cell, get_cell

from Trie import Trie, insert

#biblioteca de funcoes auxiliares
import aux_lib

##Prefixo do local das tabelas fonte para a extração de dados
prefix_loc = prefix_loc = "tabelas_mcti\\formatada\\2"

#gera um local de uma tabela fonte a cada passo
tabs = aux_lib.generate_loc(prefix_loc)

#Lista com as tabelas
lista_tabelas = []

#Cria trie
t = Trie()

#Cria lista de objetos tabela
for tabela in tabs:
    lista_tabelas.append(Table(tabela))


#Insere labes de tabela na trie
for tabela in lista_tabelas:
    insert(tabela.table_label,tabela,t.root)


t.yield_strings(t.root)

teste = t.strings_dict[t.strings_list[0]]






