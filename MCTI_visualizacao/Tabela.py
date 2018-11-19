#xlrd é uma biblioteca para facilitar o parsing de tabelas xls do excel
import xlrd
from collections import defaultdict



class Cell(object):
    '''Classe que representa uma celula da tabela. Recebe um objeto do tipo sheet do xrld como entrada
        e uma posicao X referente a linha e Y referente a celula. Cria um objeto do tipo celula classificando o tipo de celula e guardando dados'''
    def __init__(self,sheet,X,Y):

        
        ###Inicializa celula, definindo atribuitos e o tipo da celula
        #self.cell_type define o tipo da variavel:
        #Tipos possiveis: Leaf -> Representa uma celula do excel contendo dados e mais nada. É relacionada a duas chaves, uma de linha(key) e outra de coluna(key_col)
        #               : Key_Row -> Representa uma chave que ordena outras chaves(exemplo: ANO). Uma por tabela
        #                 Key_Col ->Representa uma chave que dá sentido a uma coluna. Podem existir varias por tabela
        #                 Key -> Representa uma chave presente em uma Key_col
        #                 Super_Key -> Representa uma chave que é pai de outras chaves ou de uma chave coluna. 
        #                 Label -> Representa o nome da tabela, é a raiz da arvore e pai de todos os outros nodos
        #                 Merge -> Representa uma celula que foi unida uma outra celula e não tem dados
        #                 Blank ->Não faz parte da tabela, dado vazio que pode ser removido sem alterações

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
        self.bounds = (X,X+1,Y,Y+1)
        self.cell_type = '0' #indica tipo ainda não classificado
        self.data = sheet.cell_value(rowx=X, colx=Y)




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
                    


        #Se não é um merge e nem é raiz
        if (self.cell_type == '0') and not( (Y == 0) and (Y == 0)) :
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
        else:
            #Se é raiz, é raiz
            self.cell_type = 'Label'
        
  
##########    
##########

class Table(object):
    """Classe que representa uma tabela"""

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

        #Gera tabela logica
        for X in range(self.raw_sheet.nrows):
            for Y in range (self.raw_sheet.ncols):
                self.table_data[X][Y] = Cell(self.raw_sheet,X,Y)




        
        


            
            
        

            
                
                 


                    







                




        











