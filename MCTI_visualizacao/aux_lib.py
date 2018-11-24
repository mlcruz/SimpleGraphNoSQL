##Biblioteca com funções auxiliares para o trabalho

#importa classe tabela e suas funções relacionadas
from Tabela import RawTable, Cell, get_cell, Table, get_name, normalize, get_name_labelless

#Importa Trie suas funções relacionadas
from Trie import Trie, insert, walk_to, generate_reverse_trie, moonwalk_to, prefix_search, get_all_data, get_label

#Persistencia
import dill

#Lista diretorios
from os import listdir


#Gerador para numeros de tabelas
def generate_num(tab_loc):
    '''Gera o nome do arquivo de tabela a cada passo'''
    
    index = 0
    
    #lista com todos os nomes das tabelas
    tables = listdir(tab_loc)
    l_tab = len(tables)

    while (index < l_tab):
        
        yield tables[index]
        index = index + 1

    return 0

#Gerador para locais de tabela a partir da pasta fonte da tabelas
def generate_loc(tab_loc):
    """Gera o local da tabela a cada passo"""
    
    tabs = generate_num(tab_loc)
    loc = tab_loc+"\\"
    get = next(tabs)
    

    while(get != 0):
        yield loc+get
        get = next(tabs)

def save_trie(trie,loc):
    '''Cria um arquivo em disco representando a Trie contendo todos os dados como um arquivo binario. Pode ser revertido com load_trie
        Recebe uma trie e um local para salvar o arquivo'''
    
    with open(loc,'wb') as file:
        dill.dump(trie.strings_dict,file)

def load_trie(loc):
    '''Recebe um arquivo de memoria contendo um objeto gerado por save_trie e retorna uma trie com dos dados'''
    with open(loc,'rb') as file:
        data_dict = dill.load(file)

    #Cria trie a partir do dicionario unpicklado
    t = Trie()

    for key in data_dict:
        insert(key,data_dict[key],t.root)

    t.yield_strings(t.root)
    #Retorna trie
    return t

def generate_db_trie(loc):
    '''Recebe um local de pasta contendo tabelas pre formatadas e gera uma trie contendo as tabelas como folha e os caracteres das labels como nodo
       Retorna trie gerada
    '''
    
    #gera um local de uma tabela fonte a cada passo
    tabs = generate_loc(loc)

    #Lista com as tabelas
    list_tables = []

    #Cria trie
    t = Trie()

    #Cria lista de objetos tabela
    for tabela in tabs:
        list_tables.append(Table(RawTable(tabela)))

    #Insere labels de tabela na trie
    for tabela in list_tables:
        insert(tabela.table_label,tabela,t.root)

    #Preenche dicionario de acesso da trie e outros com strings pertencentes a mesma
    t.yield_strings(t.root)

    #Gera trie reversa para busca por sufixo
    generate_reverse_trie(t)
        
    return t

