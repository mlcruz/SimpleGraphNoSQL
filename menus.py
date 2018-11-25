#Arquivos contendo os menus do programa. Cada menu recebe um strscr e um dicionario de estados, e os gerencia conforme a necessidade.

import curses
import aux_lib
import easygui

from db import DB
from collections import defaultdict
import os


from aux_lib import write_stdscr, write_stdscr_a

class Container(object):
    '''Classe representando um objeto que pode ser um Nodo ou uma Tabela ou uma Lista de celulas ou uma Celula. data representa o objeto a gerar o container
    '''

    def __init__(self,data):
        #Guarda tipo do objeto
        self.raw_type = type(data)
        self.name = ""
        self.data = 0
        self.type = ""



        #Inicializa nome e dados dependo do tipo
        if self.raw_type == aux_lib.Nodo:
            #Se é um nodo de uma trie
            self.name = "(" + aux_lib.get_label(data) + ")->"
            self.data = data
            self.type = "Node"
            

        elif self.raw_type == aux_lib.Table:
            #Se é uma tabela
            self.data = data
            self.name = data.table_label
            self.type = "Table"
             
        
        elif self.raw_type == list:
            #Se é uma lista de celulas
            self.data = data
            parent = data[0].parent_node
            self.name = aux_lib.get_name(parent) + "->[]"
            self.type = "Cell List"
        
        elif self.raw_type == aux_lib.Cell:
            #Se é uma celula
            self.data = data
            self.name = aux_lib.get_name_labelless(data)
            self.type = "Cell"
        
        elif self.raw_type == type(defaultdict()) or self.raw_type == type(dict()) or self.raw_type == type(defaultdict(dict)):
            #Se é um dicionario
            self.data = data
            data_string = ""

            key = list(data.keys())[0]
            value = list(data.items())[0]

            data_string = data_string + '{0} : {1} and others'.format(str(key),str(type(value)))

            self.name = "".join(list(data_string)[0:108])
            self.type = "Data Dict"

def start_menu(state_dict):
    '''Função que representa o menu inicial e seus estados'''
    #Strings de menus e seus locais na tela em tuplas
    str_menu_inicial = "Select option:\n1:Generate database from tables\n2:Load database from object file\n0:Exit"
    


    print(str_menu_inicial)
    c = input()
    os.system('cls')
    f_exit = False


    if c == '1':
        #Trie de tabelas
        state_dict['loc'] = easygui.diropenbox("Select directory")
        state_dict['table_trie'] = aux_lib.generate_table_trie(state_dict['loc'])
        state_dict['db'] = DB(state_dict['table_trie'])

    elif c == '2':
        state_dict['loc'] = easygui.fileopenbox("Select object file",filetypes = "*.obj")
        state_dict['table_trie'] = aux_lib.load_trie(state_dict['loc'])
        state_dict['db'] = DB(state_dict['table_trie'])

    else:
        state_dict['f_exit'] = True

    #Muda estado para menu principal
    state_dict['state'] = 'main_menu'

    #Cria estado de containers
    state_dict['containers'] = dict()

    t = state_dict['db'].tables.strings_dict[state_dict['db'].tables.strings_list[0]]
    state_dict['containers']['a'] = Container(t)
    state_dict['containers']['b'] = Container(t.table_data[8][0].child_nodes)
    state_dict['containers']['c'] = Container(t.table_data[8][3])

    state_dict['containers']['d'] = Container(state_dict['db'].tables.strings_dict)
    
    state_dict['containers']['n'] = Container(aux_lib.walk_to(state_dict['db'].tables.root,'brasil: dispendio nacional em ciencia e tecnologia (c&t) por atividade'))
    
def main_menu(stdscr, state_dict):
    '''Função que representa o menu principal e seus estados'''
    
    
    curses.cbreak()
    curses.noecho()

    #Strings e locais

    str_menu_inicial = "1:Access Table\n2:Search DB\n3:Search Table\n9:Save Current DB\n0:Exit"
    loc_menu_inicial = (0,0)

    str_saving = "Saving db...\n"
    loc_saving = (4,40)

    str_done = "Done\n"
    loc_done = (4,80)


    #Controle de loop
    local_exit = False

    #loop de repl local
    while(local_exit == False):
        #limpa
        clear_menu_area(stdscr)
       
       #escreve menu na tela
        write_stdscr(stdscr,str_menu_inicial,loc_menu_inicial)

        stdscr.move((state_dict['loc_data_entry'])[0],(state_dict['loc_data_entry'])[1])

        draw_state(stdscr,state_dict)
        #Entrada do usuario
        c = stdscr.getch()

        #Trata letras de a até z
        if (c > 140) and (c < 173):
            #Se é letra, cria container no dicionario de containers
            state_dict['containers'][chr(c)] = Container()
        if chr(c) == '1':
            access_table(stdscr, state_dict)
        if chr(c) == '2':
            search_db(stdscr, state_dict)
        if chr(c) == '0':
            state_dict['f_exit'] = True
            local_exit = True
        elif chr(c) == '9':
            loc = easygui.filesavebox('Select location for obj file')
        
            #Salva trie

            write_stdscr(stdscr,str_saving,loc_saving)
            write_stdscr(stdscr,"                      \n                      ",loc_done)
            aux_lib.save_trie(state_dict['table_trie'],loc)
            write_stdscr(stdscr,str_done,loc_done)

    
    curses.nocbreak()
    curses.echo()

def access_table(stdscr,state_dict):
    '''Menu representando as opções de accesso a tabela'''

    curses.cbreak()
    curses.noecho()

    str_access_menu = "[a-z]: Container containing a table object\n0:back"
    loc_access_menu = (0 ,0)

    str_table_menu = ''
    local_exit = False

    while(local_exit == False):

        clear_menu_area(stdscr)
        write_stdscr(stdscr,str_access_menu,loc_access_menu)
        c = stdscr.getch()
        
        #Trata letras de a até z
        if (c > 96) and (c < 123):
             current_table = state_dict['containers'][chr(c)]
             draw_table(stdscr,current_table)
             c = stdscr.getch()

        elif chr(c) == '0':
            local_exit = True

        



    

def search_db(stdscr, state_dict):
    '''Menu representando as opções de busca no banco de dados'''

    curses.nocbreak()
    curses.echo()

    str_menu_db = "1:Search Table trie\n2:Search Key_cols\n3:Seach Key_rows\n4:Search Super_keys"

def draw_state(stdscr, state_dict):
    '''Desenha gui na tela e atualiza os estados visiveis ao usuario'''

    

    #Linha separando input do usuario
    str_user_input_line = drawline(72) + "User input area" + drawline(72)
    loc_user_input_line = (50,0)

    #Linha seperando area de estados
    str_state_area_line = drawbar(50) + "+"
    loc_state_area_line = (0,120)

    #Linha separando area de tabela
    loc_table_area_line = (10,0)
    str_table_area_line = drawline(53) + "Table data area" + drawline(52) + "+"

    #Linha horizontal de estados
    loc_h_state_area_line = (0,120)
    str_h_state_area_line = "+" + drawline(12) + "Container area" + drawline(13)

    #Area de estados vai de (0,120) até (49,120)
    #Total = 40*50 = 2000 caracteres para a area de estados
    #Divididos em 10 celulas de 48*4
    
    loc_first_container = (1,122)

    offset_container_y = 6


    #Trata x e y do container como offset de loc_fisrt container
    for n,tuple in enumerate(state_dict['containers'].items()):
        #Desenha containers
        
        key = tuple[0]
        value = tuple[1]



        current_offset = offset_container_y * n
        str_current_conteiner_label = "Container " + str(key) + ":"
        
        str_current_conteiner_name = list(value.name)
        str_current_conteiner_name_1 = "".join(str_current_conteiner_name[0:36])
        str_current_conteiner_name_2 = ''.join(str_current_conteiner_name[36:72])
        str_current_conteiner_name_3 = ''.join(str_current_conteiner_name[72:108])
        str_line = drawline(39)

        str_current_conteiner_type = "Type : " + value.type

        loc_current_conteiner_label = (loc_first_container[0] + current_offset,loc_first_container[1]-1)
        loc_current_conteiner_name_1 = (loc_first_container[0] + current_offset +1,loc_first_container[1])
        loc_current_conteiner_name_2 = (loc_first_container[0] + current_offset +2,loc_first_container[1])
        loc_current_conteiner_name_3 = (loc_first_container[0] + current_offset +3,loc_first_container[1])
        loc_current_conteiner_type = (loc_first_container[0] + current_offset + 4,loc_first_container[1])
        loc_line = (loc_first_container[0] + current_offset + 5,loc_first_container[1]-1)

        write_stdscr(stdscr,str_current_conteiner_label, loc_current_conteiner_label)
        write_stdscr(stdscr,str_current_conteiner_name_1,loc_current_conteiner_name_1)
        write_stdscr(stdscr,str_current_conteiner_name_2,loc_current_conteiner_name_2)
        write_stdscr(stdscr,str_current_conteiner_name_3,loc_current_conteiner_name_3)
        write_stdscr(stdscr,str_current_conteiner_type,loc_current_conteiner_type)
        write_stdscr(stdscr,str_line,loc_line)


    write_stdscr(stdscr,str_user_input_line,loc_user_input_line)
    write_stdscr(stdscr,str_state_area_line,loc_state_area_line)
    write_stdscr(stdscr,str_table_area_line,loc_table_area_line)
    write_stdscr(stdscr,str_h_state_area_line,loc_h_state_area_line)


def drawline(intr):
    '''Returns the '-' char repeated n times in a string'''
    returns = ''
    for x in range(intr):
        returns = returns + '-'
    return returns

def drawbar(intr):
    '''Returns the '-' char repeated n times in a string'''
    returns = ''
    for x in range(intr):
        returns = returns + '|\n'
    return returns

def clear_menu_area(stdscr):
    str_clr_menu_area = "                                                                                                                        \n                                                                                                                        \n                                                                                                                        \n                                                                                                                        \n                                                                                                                        \n                                                                                                                        \n                                                                                                                        \n                                                                                                                        \n                                                                                                                        \n                                                                                                                        \n"
    loc_clr_menu_area = (0,0)
    write_stdscr(stdscr,str_clr_menu_area,loc_clr_menu_area)


def draw_table(stdscr,table_container):
    '''Draw a table in the table area from table_container data'''

    table = table_container.data

    ##Table area: From 10,0 to 55,120
    #upper_x = (13,3)
    #lower_x = (upper_x[0]+table.bound_x,3)

    #upper_y = (upper_x[0]+1,upper_x[1])
    #lower_y = (upper_x[0]+1,)
    cell_size = 5

    #Linhas e barras da tabela
    table_line = "+" + drawline(table.bound_y * (cell_size+2) - 1) + "+"
    table_bar = drawbar(table.bound_x +1)

    loc_upper_table_line = (13,3)
    loc_lower_table_line = (13+table.bound_x+2,3)

    loc_left_bar = (14,3)
    loc_right_bar = (14,(table.bound_y) * (cell_size+2) + 3)

    write_stdscr(stdscr,table_line,loc_upper_table_line)
    write_stdscr(stdscr,table_line,loc_lower_table_line)
    
    write_stdscr(stdscr,table_bar,loc_left_bar)
    write_stdscr(stdscr,table_bar,loc_right_bar)

    for X in range(table.bound_x):
        for Y in range (table.bound_y):
            loc = (loc_upper_table_line[0]+X+1,1+loc_upper_table_line[1]+Y*6)
            
            write_stdscr(stdscr," "+ str(table.table_data[X][Y].data)[:cell_size] + " ",loc)










    


