#Default dict para implementar tries
from collections import defaultdict
from Tabela import normalize

import regex

class Nodo(object):
    '''Representa um nodo de uma trie'''

    def __init__(self,char_data, data):
        '''Inicializa nodos com dados. char_data é o caractere, e data são os dados ligados aquele nodo. Representar nenhum dado como 0 '''
        #Filhos do nodo
        self.child = defaultdict(dict)

        #Pai do nodo. 0 indica raiz, -1 não atribuido
        self.parent = -1

        #0 em chard indica raiz
        self.chard = char_data
        self.data = data


class Trie(object):
    """Implementa uma Trie para pesquisa no nome de tabelas de maneira eficiente"""
    def __init__(self):
        '''Inicializa raiz da trie como um defaultdict com uma factory de dicionarios'''
        #A ideia aqui é representar uma Trie como grupos de dicionarios aninhados.
        self.root = Nodo(0,0)
        
        #Strings resultados da ultima busca da função yield_strings. Formato de dicionario para acesso mais eficiente
        self.strings_dict = defaultdict()

        #Formato de lista para acesso sequencial caso necessario
        self.strings_list = []

        #Apontador futuro para trie reversa
        self.reverse = -1
        
    def yield_strings(self,trie):
        self.strings_dict.clear()
        self.strings_list.clear()
        self.__yield_strings_aux(trie)
        return self.strings_dict


    def __yield_strings_aux(self,trie,string = "" ):
        """Retorna todas as palavras na trie especificada. Usa como criterio de ser palavra a existencia de um "dados" não nulo"""
    
        if(trie.data != 0):
            #Ao encontrar uma folha, cria uma chave para um dicionario com a string da folha como chave e os dados como valor
            self.strings_dict[string] = trie.data

            #Cria uma lista de strings encontradas
            self.strings_list.append(string)

        elif(not bool(trie.child)):
            print("fim nodo - {0}".format(string))

        else:
            key_list = trie.child.keys()
            for key in key_list:
                self.__yield_strings_aux(trie.child[key],string+key)

def insert(string, data, n_trie):
    '''Insere a string como chave ligada a um dado no ultimo nodo da trie especificada'''
    char_list = list(normalize(string.lower()))
        
    #Define proximo pai como nodo atual
    current_parent = n_trie

    #Recursivamente insere na lista
    #Se a lista não esta no ultimo elemento, inseere recursivamente começando pelo primeiro caractere
    if(len(char_list) != 1):


        #testa se o nodo referente ao primeiro caractere existe. Se nao existir, retorna um dicionario vazio(ver defaultdict)
        current_child = n_trie.child[char_list[0]]
        


        #testa se o filho tem dados antes de gravar 0. Se não é vazio, existe um nodo no filho
        if(current_child):
            #Testa se os dados são vazios no nodo filho
            #Se os dados não são vazios, vai pro proximo nodo sem inserir

            #Remove primeiro caractere da lista de caracteres
            first_char = char_list.pop(0)

            #Chamada recursiva na string sem o primeiro char
            insert(''.join(char_list),data,n_trie.child[first_char])
        else:
            #Se é vazio, cria nodo no local e insere no proximo char
            n_trie.child[char_list[0]] = Nodo(char_list[0],0)

            #Aponta pai do nodo
            n_trie.child[char_list[0]].parent = current_parent
            
            #Remove primeiro caractere da lista de caracteres
            first_char = char_list.pop(0)

            #Chamada recursiva na string sem o primeiro char
            insert(''.join(char_list),data,n_trie.child[first_char])

    else:
        #Se está na ultima letra, fim
        first_char = char_list.pop(0)
        n_trie.child[first_char] = Nodo(first_char,data)
        n_trie.child[first_char].parent = current_parent

def generate_reverse_trie(trie):
    '''Recebe uma trie e retorna a trie reversa(para busca por sufixo)
    '''
    
    #Cria trie de retorno
    t = Trie()

    #Insere na trie os dados da trie original, mas com o nome reverso
    for key in trie.strings_dict:
        insert(key[::-1],trie.strings_dict[key],t.root)

    t.yield_strings(t.root)

    #aponta tries reversas uma para a outra
    t.reverse = trie
    trie.reverse = t

    #Retorna trie
    return t     
    
def walk_to(n_trie, string):
    '''Caminha a string no nodo da trie até o nodo onde termina a string recebida. Retorna o nodo destino ou -1 em caso de falha'''
    
    #Lista de caracteres a inserir
    char_list = list(normalize(string.lower()))
    #Se a lista não está vazia
    if (char_list):
        first_char = char_list.pop(0)
        #Se existem nodos filhos
        if (n_trie.child[first_char]):
            return walk_to(n_trie.child[first_char],"".join(char_list))
        else:
            return -1
    else:
        #Se de caracteres está vazia, chegou no fim
        return n_trie

def moonwalk_to(nodo, string):
    '''Caminha a string do fim pro começo saindo do nodo e indo no sentido da raiz. Retorna o nodo destino ou -1 em caso de falha'''
    
    #Lista de caracteres a inserir
    char_list = list(normalize(string.lower()))

    #Se a lista não está vazia
    if (char_list):
        last_char = char_list.pop()
        
        #Se existem nodos pai que satisfazem o ultimo caractere removido(após normalização)
        if (nodo.parent.chard == normalize(last_char)):
            return moonwalk_to(nodo.parent,"".join(char_list))
        #Se raiz
        elif (nodo.parent.chard == 0):
            return 0
        else:
            return -1
    else:
        #Se de caracteres está vazia, chegou no fim
        return nodo

def get_label(nodo, string = ""):
    '''Caminha um nodo no sentido nodo raiz até a raiz e devolve os caracteres encontrados no camniho'''
    if nodo.chard == 0:
        #Se é raiz, termina
        return string
    else:
        string =  nodo.chard + string 
        return get_label(nodo.parent, string)

def prefix_search(trie, string):
    '''Retorna o dicionario {label,data} de todos os objetos encontrados, usando a string recebida como prefixo para buscar na trie recebida
    '''
    
    #Caminha até string
    w = walk_to(trie.root,string)
 
    #Recebe dados
    data = get_all_data(w)

    return data

def suffix_search(trie, string):
    '''Retorna o dicionario {label,data} de todos os objetos encontrados, usando a string recebida como sufixo para buscar na trie recebida'''

    #String revertida
    r_string = string[::-1]

    #Caminha até a string na arvore reversa
    w = walk_to(trie.reverse.root,r_string)

    #Retorna dados
    r_data = get_all_data(w)

    data = defaultdict()

    #Reverte a chave dos dados retornados
    for key, value in r_data.items():
        data[''.join(list(key)[::-1])] = value

    return data

def regex_search(trie, re_string):
    '''Pesquisa expressão regular na trie recebida. Retorna dicionario de todos os nodos onde a chave contem o valor da expressão'''
    data = get_all_data(trie.root)
    matched = defaultdict()

    c_pattern = regex.compile(re_string)

    for key, value in data.items():
        if (bool(c_pattern.findall(key))):
            matched[key] = value
    return matched


def regex_dict_search(dict, re_string):
    '''Pesquisa expressão regular no default dict em formato de trie recebido. Retorna dicionario de todos os nodos onde a chave contem o valor da expressão'''
    data = dict
    matched = defaultdict()

    c_pattern = regex.compile(re_string)

    for key, value in data.items():
        if (bool(c_pattern.findall(key))):
            matched[key] = value
    return matched





def get_all_data(n_trie ,r_type = 'dict'):
    '''Recebe um nodo de trie e Retorna dicionario no formato {label,table} contendo todos os dados não nulos da trie especificada. Se r_type = 'list', retorna uma lista em vez de um dict'''
    
    #Dicionario para receber resultados da função auxliar
    def_dict = defaultdict(dict)

    #list para dados
    def_list = []

    #Pega label do nodo encontrado
    w_label = get_label(n_trie)

    __get_all_data_aux(n_trie,def_dict,def_list,w_label)


    if r_type == 'dict':
        return def_dict
    else:
        return def_list

def __get_all_data_aux(n_trie,def_dict,def_list,label,string = ""):
    """Auxiliar para get_all data. Insere na lista recebida todas as palavras no nodo da trie especificada. Usa como criterio de ser palavra a existencia de "dados" não nulos"""   
    if(n_trie.data != 0):
        #Ao encontrar uma folha, cria uma chave para um dicionario com a string da folha como chave e os dados como valor
        def_dict[label+string] = n_trie.data

        #Cria uma lista de strings encontradas
        def_list.append(label+string)

    elif(not bool(n_trie.child)):
        print("fim nodo - {0}".format(string))

    else:
        key_list = n_trie.child.keys()
        for key in key_list:
            __get_all_data_aux(n_trie.child[key],def_dict,def_list,label,string+key)






             
            

            





