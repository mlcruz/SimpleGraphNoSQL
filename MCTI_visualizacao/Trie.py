#Default dict para implementar tries

from collections import defaultdict


class Nodo(object):
    '''Representa um nodo de uma trie'''

    def __init__(self,char_data, data):
        '''Inicializa nodos com dados. char_data é o caractere, e data são os dados ligados aquele nodo. Representar nenhum dado como 0 '''
        self.child = defaultdict(dict)
        #0 em chard indica raiz
        self.chard = char_data
        self.data = data


class Trie(object):
    """Implementa uma Trie para pesquisa de no nome de tabelas de maneira eficiente"""
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
    '''Insere a string no ultimo nodo da trie especificada'''
    char_list = list(string)
        
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
            last_char = char_list.pop(0)

            #Chamada recursiva na string sem o primeiro char
            insert(''.join(char_list),data,trie.child[last_char])
        else:
            #Se é vazio, cria nodo no local e insere no proximo char
            trie.child[char_list[0]] = Nodo(char_list[0],0)
                    
            #Remove primeiro caractere da lista de caracteres
            last_char = char_list.pop(0)

            #Chamada recursiva na string sem o primeiro char
            insert(''.join(char_list),data,trie.child[last_char])

    else:
        #Se está na ultima letra, fim
        last_char = char_list.pop(0)
        trie.child[last_char] = Nodo(last_char,data)








             
            

            





