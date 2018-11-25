#Arquivos contendo os menus do programa. Cada menu recebe um strscr e um dicionario de estados, e os gerencia conforme a necessidade.

import curses
import aux_lib
import easygui

from db import DB
from collections import defaultdict
import os


from aux_lib import write_stdscr, write_stdscr_a
import curses.textpad

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
            parent_list = []
            for item in data:
                if (item.cell_type != "Blank") and (item.cell_type != "Merge"):
                    parent_list.append(item.parent_node)

            #Se todos os nodos tem o mesmo pai, aponta para chave
            if len(set(parent_list)) == 1:
                parent = data[0].parent_node
                self.name = aux_lib.get_name(parent) + "->[]"
            else:
                parent = data[0].key_col
                self.name = aux_lib.get_name_labelless(parent) + "->[]"
            
            
            
            self.type = "Cell_List"
        
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
            self.type = "Data_Dict"

##Menus
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

    state_dict['containers']['g'] = Container(t.table_data[3][2].child_nodes)
    state_dict['containers']['s'] = Container(t.table_data[1][1].child_nodes)
    state_dict['containers']['k'] = Container(t.table_data[1][0].child_nodes)
    
def main_menu(stdscr, state_dict):
    '''Função que representa o menu principal e seus estados'''
    
    
    curses.cbreak()
    curses.noecho()

    #Strings e locais

    str_menu_principal = "[a-z]:Draw container\n1:Access Table\n2:Search DB\n3:Search Table\n9:Save Current DB\n-:clear table area\n0:Exit"
    loc_menu_principal = (0,0)

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
        write_stdscr(stdscr,str_menu_principal,loc_menu_principal)

        stdscr.move((state_dict['loc_data_entry'])[0],(state_dict['loc_data_entry'])[1])

        draw_state(stdscr,state_dict)
        #Entrada do usuario
        c = stdscr.getch()

        #Trata letras de a até z
        if (c > 96) and (c < 123):
            #Se é letra, desenha container
            draw_container(stdscr,state_dict['containers'][chr(c)])
        if chr(c) == '-':
            clear_table_area(stdscr)

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

    str_access_menu = "[a-z]: Container containing a table object\n1:Query Table\n6:Set Container\n0:back"
    loc_access_menu = (0 ,0)
    set_container = ""


    str_last_container = "Output Container: ["+set_container+"]"
    loc_last_container = (7,0)
    str_selected_table = "Selected table: []"
    loc_selected_table = (8,0)

    str_table_menu = ''
    local_exit = False

    while(local_exit == False):

        clear_menu_area(stdscr)
        write_stdscr(stdscr,str_access_menu,loc_access_menu)
        write_stdscr(stdscr,str_selected_table,loc_selected_table)
        write_stdscr(stdscr,str_last_container,loc_last_container)
        
        c = stdscr.getch()
        
        #Trata letras de a até z
        if (c > 96) and (c < 123):
             current_table = state_dict['containers'][chr(c)].data
             str_selected_table = "Selected table: ["+ current_table.table_label +"]"
             write_stdscr(stdscr,str_selected_table,loc_selected_table)

             draw_container(stdscr,state_dict['containers'][chr(c)])



             c = stdscr.getch()

        elif chr(c) == '0':
            local_exit = True
        elif chr(c) == '6':
            write_stdscr(stdscr,"Press any key to save as container key",(4,60))
            c = stdscr.getch()
            set_container = chr(c)
            str_last_container = "Output Container: ["+set_container+"]"
        elif chr(c) == '1':

            #Inicializa tratamento de querry
            curses.nocbreak()
            curses.echo()

            stdscr.keypad(True)
            #restore_cursor(stdscr,state_dict)
            clear_input_area(stdscr)
           
            write_stdscr(stdscr,"Enter Query. CTRL+G to exit. Control-H	to delete",(51,40))
            
            Entrada = get_input(stdscr)
            

            



def get_input(stdscr):
            input_area = curses.newwin(1, 118, 53, 1)
            ret_input_box = curses.textpad.rectangle(stdscr,52,0,54,120)
            input_box = curses.textpad.Textbox(input_area)
            stdscr.refresh()

            input_txt = input_box.edit()
            stdscr.keypad(False)

            #Por algum motivo as strings vem duplicadas. Trata esse bug(?)
            input_txt = list(str(input_txt).rstrip().lstrip())
            metade = int(len(input_txt)/2)

            input_txt = "".join(input_txt[:metade])

            #Limpa area de input
            stdscr.refresh()
            clear_input_area(stdscr)
            curses.cbreak()
            curses.noecho()
            restore_cursor(stdscr)
            return input_txt






     
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




##Funcions
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

def clear_table_area(stdscr):
    ##Table area: From 10,0 to 50,120
    str_clr_table_line = "                                                                                                                      \n"
    str_clr_table_line_x_5 = str_clr_table_line + str_clr_table_line + str_clr_table_line + str_clr_table_line + str_clr_table_line
    str_clr_table_area =  str_clr_table_line_x_5 + str_clr_table_line_x_5 + str_clr_table_line_x_5 + str_clr_table_line_x_5 + str_clr_table_line_x_5 + str_clr_table_line_x_5 + str_clr_table_line_x_5 + str_clr_table_line + str_clr_table_line + str_clr_table_line
    loc_clr_table_area = (11,0)

    write_stdscr(stdscr,str_clr_table_area,loc_clr_table_area)

def clear_input_area(stdscr):
    #Input é do 50,0 ao 55,120
    str_clr_table_line = "                                                                                                                         \n"
    str_clr_table_line_x_4 = str_clr_table_line + str_clr_table_line + str_clr_table_line + "                                                                                                                         "
    loc_clr_table_area = (51,0)
    write_stdscr(stdscr,str_clr_table_line_x_4,loc_clr_table_area)

def draw_table(stdscr,table_container):
    '''Draw a table in the table area from table_container data'''
    
    table = table_container.data

    ##Table area: From 10,0 to 50,120


    cell_size = int(110/(table.bound_y + 2))



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
            loc = (loc_upper_table_line[0]+X+1,1+loc_upper_table_line[1]+Y*cell_size)
            
            write_stdscr(stdscr," "+ str(table.table_data[X][Y].data)[:cell_size] + " ",loc)

def draw_cell(stdscr, y ,x , container):
    '''Desenha celula na tela'''
    


    #+-------------------
    #|Key_row   | Key_Col
    #|-------------------
    #|Key[-len-]| Data
    #+-------------------
    cell_container = container.data

    if (cell_container.cell_type != 'Blank') and (cell_container.cell_type != 'Merge') :

        
        if(cell_container.cell_type == "Key"):
            data = "<Cell.child_nodes>"
            key_row_data = str(cell_container.parent_node.data)
            key = str(cell_container.data)
            key_col_data = "Data"
   
        else:

            key_col_first_parent = cell_container.key_col.parent_node
            key_col_second_parent = key_col_first_parent.parent_node
    
            key_col_label_t = str(aux_lib.get_name(cell_container))

            #Label truncada par 6 char
            key_col_label_t = "".join(list(key_col_label_t)[:5])

            #Segundo pai trunkado para 6 char
            key_col_second_parent_t = str(key_col_second_parent.data)
            key_col_second_parent_t = "".join(list(key_col_second_parent_t)[:5])

            #Primeiro pai trunkada para 8 char
            key_col_first_parent_t = str(key_col_first_parent.data)
            key_col_first_parent_t = "".join(list(key_col_first_parent_t)[:8])

            #Se segundo pai é label
            if(key_col_label_t == key_col_second_parent_t):
                key_col_data = key_col_label_t + "-" + key_col_first_parent_t + "-" + str(cell_container.key_col.data)
            else:
                key_col_data = key_col_label_t + "-" + key_col_second_parent_t + "-" + key_col_first_parent_t + "-" + str(cell_container.key_col.data)


        #key_col_data = str(cell_container.key_col.data)
            key_row_data = str(cell_container.key_row.parent_node.data)
            data = str(cell_container.data)

            key = str(cell_container.parent_node.data)

        key_len = len(list(key))
        data_len = len(list(data))
    

        #Trunka tamanhos
        key_col_data = "".join(list(key_col_data)[:(38 - (key_len+1))])

        key_row_data = "".join(list(key_row_data)[:key_len])

        ##Table area: From 10,0 to 50,120
        loc_upper_cell_line = (y,x)
        loc_middle_cell_line = (y+2,x)
        loc_lower_cell_line = (y+4,x)
        loc_left_bar = (y,x)
        loc_right_bar = (y,x+38)
        loc_middle_bar = (y,x+key_len+1)
    
        str_middle_bar = "-\n|\n-\n|\n-"
        str_line = drawline(38)
        str_bar = "+\n" +drawbar(3) + "+\n"

        write_stdscr(stdscr,key_row_data,(loc_left_bar[0] + 1, loc_left_bar[1] + 1))
        write_stdscr(stdscr,key_col_data,(loc_left_bar[0] + 1, loc_middle_bar[1] + 1))
        write_stdscr(stdscr,key,(loc_left_bar[0] + 3, loc_left_bar[1] + 1))
        write_stdscr(stdscr,data,(loc_left_bar[0] + 3, loc_middle_bar[1] + 1))
        write_stdscr(stdscr,str_line,loc_upper_cell_line)
        write_stdscr(stdscr,str_line,loc_middle_cell_line)
        write_stdscr(stdscr,str_line,loc_lower_cell_line)
        write_stdscr(stdscr,str_bar,loc_right_bar)
        write_stdscr(stdscr,str_bar,loc_upper_cell_line)
        write_stdscr(stdscr,str_middle_bar,loc_middle_bar)

def draw_container(stdscr, container):
    '''Desenha container na tela, na area de tabela'''
    if container.type == 'Table':
        clear_table_area(stdscr)
        draw_table(stdscr,container)
    if container.type == 'Cell':
        clear_table_area(stdscr)
        draw_cell(stdscr,13,3,container)
    if container.type == 'Cell_List':
        clear_table_area(stdscr)

        #Desenha as 6 primeiras celulas se lista
        y_pos = 13

        #Limpa lista de celulas vazias

        cleaned_list = []

        for cell in container.data:
            if (cell.cell_type != "Blank") and (cell.cell_type != "Merge"):
                cleaned_list.append(cell)

        t_list = cleaned_list[:7]
        y_list = cleaned_list[7:15]
        u_list = cleaned_list[15:23]

        for cell in t_list:
            if type(cell) == aux_lib.Cell:
                draw_cell(stdscr,y_pos,3,Container(cell))
                if (cell.cell_type != "Blank") and (cell.cell_type != "Merge"):
                    y_pos = y_pos + 4
        
        y_pos = 13

        for cell in y_list:
            if type(cell) == aux_lib.Cell:
                draw_cell(stdscr,y_pos,41,Container(cell))
                if (cell.cell_type != "Blank") and (cell.cell_type != "Merge"):
                    y_pos = y_pos + 4
        
        y_pos = 13
        for cell in u_list:
            if type(cell) == aux_lib.Cell:
                draw_cell(stdscr,y_pos,79,Container(cell))
                if (cell.cell_type != "Blank") and (cell.cell_type != "Merge"):
                    y_pos = y_pos + 4

    if container.type == "Data_Dict":
        clear_table_area(stdscr)
        y_pos = 13
        x_pos = 2
        
        for key, value in container.data.items():
            str_output = "".join(list(str(key))[:90]) + ":" + str(value)
            #trunka
            str_output = "".join(list(str_output)[:114])

            #Trata fim da tabela
            if(y_pos > 48):
                break
            
                
            
            write_stdscr(stdscr,str_output,(y_pos,x_pos))
            y_pos = y_pos + 1

def restore_cursor(stdscr,state_dict):
    stdscr.move((state_dict['loc_data_entry'])[0],(state_dict['loc_data_entry'])[1])


def restore_cursor(stdscr):
    stdscr.move(52,0)
