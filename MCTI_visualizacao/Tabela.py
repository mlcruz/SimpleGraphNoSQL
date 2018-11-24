#xlrd é uma biblioteca para facilitar o parsing de tabelas xls do excel
import xlrd

#Default dics são dicionarios que ao receber uma chave que não existe, cria a chave a atribui um valor padrão
from collections import defaultdict

#Suporte para expressões regulares
import regex

#Para normalizar para NFKD
import unicodedata


class Cell(object):
    '''Classe que representa uma celula da tabela. Recebe um objeto do tipo sheet do xrld como entrada
        e uma posicao X referente a linha e Y referente a celula. Cria um objeto do tipo celula classificando o tipo de celula e guardando dados'''
    def __init__(self,sheet,X,Y):

        
        ###Inicializa celula, definindo atribuitos e o tipo da celula
        #self.cell_type define o tipo da variavel:
        #Tipos possiveis:  Leaf -> Representa uma celula do excel contendo dados e mais nada. É relacionada a duas chaves, uma de linha(key) e outra de coluna(key_col)
        ##               : Key_Row -> Representa uma chave que ordena outras chaves(exemplo: ANO). Uma por tabela
        ##                 Key_Col ->Representa uma chave que dá sentido a uma coluna. Podem existir varias por tabela
        ##                 Key -> Representa uma chave presente em uma Key_col
        ##                 Super_Key -> Representa uma chave que é pai de outras chaves ou de uma chave coluna. 
        ##                 Label -> Representa o nome da tabela, é a raiz da arvore e pai de todos os outros nodos
        ##                 Merge -> Representa uma celula que foi unida uma outra celula e não tem dados
        ##                 Blank ->Não faz parte da tabela, dado vazio que pode ser removido sem alterações
        ################################################################################################################################





        #Atributos usados para organização da tabela:
        
        # A largura da celula raiz indica o numero de colunas da tabela
        #self.data_boudary -> Indica local da primeira chave na coluna indexadora
        #self.originx = indica local y de origem do merge
        #self.originy = indica local y de origem do merge
        #self.sizex = indica tamanho x da celula
        #self.sizex = indica tamanho y da celula

        
        #Inicializa data boundary como 2, indicando primeira chave se col_row não é merged
        self.data_boundary = 2
        self.blank_boundary = 9999
        self.originx = X
        self.originy = Y
        self.sizex = 1
        self.sizey = 1
        self.x = X
        self.y = Y
        self.bounds = (X,X+1,Y,Y+1)
        self.cell_type = '0' #indica tipo ainda não classificado
        self.data = sheet.cell_value(rowx=X, colx=Y)

        #Representa o local da celula pai da celula atual. Key_Row é pai de Key, Super_key é pai de Key_col.
        #Inicializado com -1 para indicar que ainda não está atribuido. Somente para não folhas
        self.parent_node = -1


        #Lista representando todos os nodos filhos da celula. Somente para não folhas
        self.child_nodes = []

        #Variaveis representando as chaves de ordenação da celula.
        self.key_row = -1
        self.key_col = -1
        
        #Variavel representando nome completo da celula, que leva em conta as chaves que à ordenam e sua label da tabela
        self.cell_name = ""


        #Calcula tamanho da celula, merges e data boundaries da folha.
        for merged in sheet.merged_cells:
       
            #Calcula onde inicia cada campo de dados a partir do tamanho da coluna indexadora no caminho
            #Verifica se é primeiro item não label da coluna indexadora

            #Se a linha inicial é a primeira linha após a label e está na primeira coluna, é key_row da tabela
            if (merged[0] == 1) and (merged[2] == 0):
                
                #Define limite local onde iniciam os dados da tabela(em contrapartida com os outros tipos de celula acima)
                #Lembrando que data_boundary indica o local do primeiro item do tipo chave na coluna indexadora
                self.data_boundary = merged[1]

            #Se é raiz, calcula blank_boundary definindo limites da tabela a partir do limite X da label
            if(merged[0] == 0) and (merged[2] == 0):
                self.blank_boundary = merged[3]

            #Se X e Y está entre os limites dos dados a respeito da celula merged recebida(ou seja, é uma celula unida)
            #Calcula tamanho e tipo da celula(se é do tipo merge ou outro)
            
            
            if (X >= merged[0]) and (X < merged[1]) and (Y >= merged[2]) and (Y < merged[3]):


                #Calcula a celula origem
                self.originx = merged[0]
                self.originy = merged[2]

                #Se é a celula origem
                if (X == self.originx) and (Y == self.originy):
           
                    #Calcula o tamanho da celula
                    self.sizex = merged[1] - merged[0]
                    self.sizey = merged[3] - merged[2]
                   
                    #Guarda a tupla merged para salvar os limites da celula
                    self.bounds = merged

                else:
                    #Se é uma celula unida, indica isso
                    self.cell_type = 'Merge'
                    


        #Se não é um merge e nem é raiz, classifica celula dentro dos outros tipos possiveis
        if (self.cell_type == '0') and not( (Y == 0) and (X == 0)) :
            #Se Y é menor que blank_boundary, não é blank
            if Y >= self.blank_boundary:
                self.cell_type = "Blank"

            else:
                #Se X é menor que a data_boundary, é key_col, key_row ou super_key
                if X < self.data_boundary:
                    #Se Y é 0, é key_Row
                    if Y == 0:
                        self.cell_type = 'Key_Row'
                    #Se não, é key_col ou super_key
                    else:
                        #Se tem largura 1, é Key_Col
                        if self.sizey == 1:
                            self.cell_type = 'Key_Col'
                        else:
                            self.cell_type = 'Super_Key'
                #Se é maior que a data boundary, é key ou leaf
                else:
                    #Se Y == 0, é key
                    if Y == 0:
                        self.cell_type = 'Key'
                    else:
                        self.cell_type = 'Leaf'
        elif self.cell_type == '0':
            #Se é raiz, é raiz
            self.cell_type = 'Label'
              
class RawTable(object):
    """Classe que representa uma tabela do excel na memoria. Guarda mais dados do que o necessario e não consegue ser pickleada"""

    def __init__(self, loc):
        """Inicializa uma tabela a partir de um local loc"""

        self.loc_source = loc

        #Tabela original como xls, parseada pelo xlrd
        self.raw_table = xlrd.open_workbook(loc,formatting_info=True)

        #Folha da tabela original
        self.raw_sheet = self.raw_table.sheet_by_index(0)

        #Label da tabela, primeira coluna primeira linha
        self.table_label = self.raw_sheet.cell_value(rowx=0, colx=0)

        #Representa matriz como dicionarios aninhados
        self.table_data = defaultdict(dict)
        self.bound_x = self.raw_sheet.nrows
        self.bound_y = self.raw_sheet.ncols

        #Gera tabela logica
        for X in range(self.raw_sheet.nrows):
            for Y in range (self.raw_sheet.ncols):
                self.table_data[X][Y] = Cell(self.raw_sheet,X,Y)
        
        #Gera atributos de pai, filhos e chaves de ordenação a partir do tipo da celula da tabela logica para cada celula
        for X in range(self.raw_sheet.nrows):
            for Y in range (self.raw_sheet.ncols):
                #Classifica dependendo do tipo
                if self.table_data[X][Y].cell_type == "Leaf":
                    #Se leaf, aponta celulas que ordenam a mesma
                    #Aponta celula ordenadora de linha, definida pela sua linha e coluna. 
                    self.table_data[X][Y].key_row = self.table_data[X][0]

                    #Aponta nodo pai como chave
                    self.table_data[X][Y].parent_node = self.table_data[X][Y].key_row

                    #Aponta para ordenadora de coluna, tratando merges. Indicado pela primeira linha antes da data boundary
                    self.table_data[X][Y].key_col = get_cell(self.table_data[(self.table_data[X][Y].data_boundary - 1)][Y],self.table_data)

                elif(self.table_data[X][Y].cell_type != "Key"):
                     self.table_data[X][Y].data = ((normalize(str(self.table_data[X][Y].data))).lstrip()).rstrip() 
                    #Se não é leaf nem key, normaliza data e converte para string e tira espaços
                
                if self.table_data[X][Y].cell_type == "Key":

                    
                    #Se Chave, aponta para ultimo Row_key como parente tratando merges
                    self.table_data[X][Y].parent_node = get_cell(self.table_data[(self.table_data[X][Y].data_boundary - 1)][Y],self.table_data)
                    #Aponta para todas os dados indexados por essa chave
                    for node in range(1,self.raw_sheet.ncols):
                        self.table_data[X][Y].child_nodes.append(self.table_data[X][node])

                if (self.table_data[X][Y].cell_type == "Key_Row") or (self.table_data[X][Y].cell_type == "Key_Col") or (self.table_data[X][Y].cell_type == "Super_Key"):
                    #Usa a boudary superior do merge para apontar para o pai. Pai sempre vai ser a celula acima considerando merge
                    self.table_data[X][Y].parent_node = get_cell(self.table_data[self.table_data[X][Y].bounds[0] - 1][Y],self.table_data)
                    
                    #Filhos da Key_Row/Col são as chaves abaixo da mesma
                    for node in range(self.table_data[X][Y].data_boundary,self.raw_sheet.nrows):
                        self.table_data[X][Y].child_nodes.append(self.table_data[node][Y])
               
                #Se é label         
                if self.table_data[X][Y].cell_type == "Label": 
                   #parent_node 0 pois é raiz
                   self.table_data[X][Y].parent_node = 0
                   #Filhos são todos os nodos da linha abaixo não Merge
                   for node in range(self.raw_sheet.ncols):
                       if (self.table_data[1][node].cell_type != "Merge") and (self.table_data[1][node].cell_type != "Blank"):
                           self.table_data[X][Y].child_nodes.append(self.table_data[1][node])

                
                if self.table_data[X][Y].cell_type == "Merge":
                    #Se é merge, aponta filhos e pais para o do nodo origem
                    self.table_data[X][Y].child_nodes = self.table_data[self.table_data[X][Y].originx][self.table_data[X][Y].originy].child_nodes
                    self.table_data[X][Y].parent_node = self.table_data[self.table_data[X][Y].originx][self.table_data[X][Y].originy].parent_node
          
                    

        #Completa nomes nas celulas
        for X in range(self.raw_sheet.nrows):
            for Y in range (self.raw_sheet.ncols):    
                if(self.table_data[X][Y].cell_type == "Merge"):
                    #Se é merge, completa nome dependendo do nome da origem
                    if(self.table_data[X][Y].parent_node != 0 and self.table_data[X][Y].parent_node != -1):
                    #Se não é merge da raiz, atribui nome pelo nome da origem
                        self.table_data[X][Y].cell_name = self.table_data[X][Y].parent_node.cell_name
                    else:
                        #Atribui nome da raiz se merge da raiz
                        self.table_data[X][Y].cell_name = get_cell(self.table_data[X][Y],self.table_data).data


                elif(self.table_data[X][Y].cell_type == "Label"):
                    self.table_data[X][Y].cell_name = self.table_data[X][Y]
                else:
                    #Se não é merge, atribui nome
                    self.table_data[X][Y].cell_name = get_name(self.table_data[X][Y])
                         
class Table(object):
    """Classe que representa uma tabela logica. Recebema uma Raw_Table e remove os campos desnecessarios Pode ser picklada"""

    def __init__(self, raw_table):
        '''Inicializa Tabela com dados da raw table'''
        self.loc_source = raw_table.loc_source
        self.table_label = raw_table.table_label
        self.table_data = raw_table.table_data
        self.bound_x = raw_table.raw_sheet.nrows
        self.bound_y = raw_table.raw_sheet.ncols


def normalize(input_text):
    """Normaliza String e lida com caracteres especiais. Transforma qualquer string para uma string contendo somente caracteres não acentuados
    """
    return_str = regex.sub(r'\u00DF','ss',input_text,)
    return_str = regex.sub(r'\u1E9E','SS',return_str) # scharfes S
    return_str = regex.sub(r'\u0111','d',return_str,)
    return_str = regex.sub(r'\u0110','D',return_str) # crossed D
    return_str = regex.sub(r'\u00F0','d',return_str,)
    return_str = regex.sub(r'\u00D0','D',return_str) # eth
    return_str = regex.sub(r'\u00FE','th',return_str,)
    return_str = regex.sub(r'\u00DE','TH',return_str) # thorn
    return_str = regex.sub(r'\u0127','h',return_str,)
    return_str = regex.sub(r'\u0126','H',return_str) # H-bar
    return_str = regex.sub(r'\u0142','l',return_str,)
    return_str = regex.sub(r'\u0141','L',return_str) # L with stroke
    return_str = regex.sub(r'\u0153','oe',return_str,)
    return_str = regex.sub(r'\u0152','Oe',return_str) # Oe ligature
    return_str = regex.sub(r'\u00E6','ae',return_str,)
    return_str = regex.sub(r'\u00C6','Ae',return_str) # Ae ligature
    return_str = regex.sub(r'\u0131','i',return_str,) #dotless i
    return_str = regex.sub(r'\u00F8','o',return_str)
    return_str = regex.sub(r'\u00D8','O',return_str) # o with stroke
    return_str = regex.sub(r'[\u00B7\u02BA\uFFFD]','',return_str) # Catalan middle dot, double prime
    return_str = unicodedata.normalize('NFKD',return_str)
    return_str = regex.sub(r'[\u0300-\u036f]','',return_str) #Splits string into simple characters + modifiers and remove them
    return_str = regex.sub(r'\s',' ',return_str) #remobe double whitespaces
    
    return return_str

      
def get_name_labelless(cell, string =""):
    '''Recursivamente percorre uma tabela em formato de arvore a partir de uma celula e retorna uma string com seu nome. Usa o caractere > como indicador de relacionamento pai-filho entre celulas
       Diferentemente de get_name, essa função retorna a string do nome sem o nome da raiz
        '''

    #Se é raiz, fim.
    if cell.cell_type == 'Label':
        return string
    #Se não, nome é nome do filho + > + nome do pai
    if cell.cell_type == 'Merge' or cell.cell_type == 'Blank':
        #Se é  merge/branco retorna merge vazio
        return ""
    else:
        if string == "":
            if cell.cell_type == 'Leaf':
                #Se é folha, alem do nodo pai indica a chave de coluna no nome após o da chave de linha
                return get_name_labelless(cell.parent_node,get_name_labelless(cell.key_col)+'>'+str(cell.data))
            else:
                return get_name_labelless(cell.parent_node,str(cell.data))
        else:
            return get_name_labelless(cell.parent_node,str(cell.data)+">"+string)

def get_name(cell, string =""):
    '''Recursivamente percorre uma tabela em formato de arvore a partir de uma celula e retorna uma string com seu nome. Usa o caractere > como indicador de relacionamento pai-filho entre celulas'''

    #Se é raiz, fim.
    if (cell.cell_type == 'Label') and string != "":
        return cell.data + ">" + string
    #Se não, nome é nome do filho + > + nome do pai
    if cell.cell_type == 'Merge' or cell.cell_type == 'Blank':
        #Se é  merge/branco retorna merge vazio
        return ""
    else:
        if string == "":
            if cell.cell_type == 'Leaf':
                #Se é folha, alem do nodo pai indica a chave de coluna no nome após o da chave de linha
                return get_name(cell.parent_node,get_name_labelless(cell.key_col)+'>'+str(cell.data))
            
            elif cell.cell_type == "Label":
                #Se é raiz, remove retorna sem > no fim
                return cell.data

            else:
                return get_name(cell.parent_node,str(cell.data))

        else:
            return get_name(cell.parent_node,str(cell.data)+">"+string)

def get_cell(cell,table_data):
    '''Retorna uma celula tratando merges. Recebe um objeto do tipo Cell e uma table_data de uma tabela e Sempre retorna uma celula origem, é reflixiva para celulas não merge'''
    return table_data[cell.originx][cell.originy]
        




     
            
            
        

            
                
                 


                    







                




        











