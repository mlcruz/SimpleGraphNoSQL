#Default dict para implementar tries
from collections import defaultdict
from Tabela import normalize


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


def insert(string, data, trie):
    '''Insere a string como chave ligada a um dado no ultimo nodo da trie especificada'''
    char_list = list(normalize(string.lower()))
        
    #Define proximo pai como nodo atual
    current_parent = trie

    #Recursivamente insere na lista
    #Se a lista não esta no ultimo elemento, inseere recursivamente começando pelo primeiro caractere
    if(len(char_list) != 1):


        #testa se o nodo referente ao primeiro caractere existe. Se nao existir, retorna um dicionario vazio(ver defaultdict)
        current_child = trie.child[char_list[0]]
        


        #testa se o filho tem dados antes de gravar 0. Se não é vazio, existe um nodo no filho
        if(current_child):
            #Testa se os dados são vazios no nodo filho
            #Se os dados não são vazios, vai pro proximo nodo sem inserir

            #Remove primeiro caractere da lista de caracteres
            first_char = char_list.pop(0)

            #Chamada recursiva na string sem o primeiro char
            insert(''.join(char_list),data,trie.child[first_char])
        else:
            #Se é vazio, cria nodo no local e insere no proximo char
            trie.child[char_list[0]] = Nodo(char_list[0],0)

            #Aponta pai do nodo
            trie.child[char_list[0]].parent = current_parent
            
            #Remove primeiro caractere da lista de caracteres
            first_char = char_list.pop(0)

            #Chamada recursiva na string sem o primeiro char
            insert(''.join(char_list),data,trie.child[first_char])

    else:
        #Se está na ultima letra, fim
        first_char = char_list.pop(0)
        trie.child[first_char] = Nodo(first_char,data)
        trie.child[first_char].parent = current_parent
        

def walk_to(trie, string):
    '''Caminha a string na trie da raiz até o nodo onde termina a string recebida. Retorna o nodo destino ou -1 em caso de falha'''
    
    #Lista de caracteres a inserir
    char_list = list(normalize(string.lower()))
    #Se a lista não está vazia
    if (char_list):
        first_char = char_list.pop(0)
        #Se existem nodos filhos
        if (trie.child[first_char]):
            return walk_to(trie.child[first_char],"".join(char_list))
        else:
            return -1
    else:
        #Se de caracteres está vazia, chegou no fim
        return trie

    

#def moonwalk_to(nodo, string):
    '''Caminha a string desejada saindo do nodo e indo no sentido da raiz. Retorna o nodo destino ou -1 em caso de falha'''








             
            

            





