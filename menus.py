#Arquivos contendo os menus do programa. Cada menu recebe um strscr e um dicionario de estados, e os gerencia conforme a necessidade.

import curses
import aux_lib
import easygui

from db import DB
from collections import defaultdict
import os


from aux_lib import write_stdscr, write_stdscr_a

class Container(object):
    '''Classe representando um objeto que pode ser um Nodo ou uma Tabela ou uma Lista de celulas ou uma Celula'''

    def __init__(self, data):
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
            self.name = aux_lib.get_name(data)
            self.type = "Cell"


            
        



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


    #escreve menu na tela
    write_stdscr(stdscr,str_menu_inicial,loc_menu_inicial)

    #Controle de loop
    local_exit = False

    #loop de repl local
    while(local_exit == False):
        stdscr.move((state_dict['loc_data_entry'])[0],(state_dict['loc_data_entry'])[1])

        draw_state(stdscr,state_dict)
        #Entrada do usuario
        c = chr(stdscr.getch())

        if c == '2':
            search_db(stdscr, state_dict)
        if c == '0':
            state_dict['f_exit'] = True
            local_exit = True
        elif c == '9':
            loc = easygui.filesavebox('Select location for obj file')
        
            #Salva trie

            write_stdscr(stdscr,str_saving,loc_saving)
            write_stdscr(stdscr,"                      \n                      ",loc_done)
            aux_lib.save_trie(state_dict['table_trie'],loc)
            write_stdscr(stdscr,str_done,loc_done)

    
    curses.nocbreak()
    curses.echo()



def search_db(stdscr, state_dict):
    '''Menu representando as opções de busca no banco de dados'''

    curses.nocbreak()
    curses.echo()

    str_menu_db = "1:Search Table trie\n2:Search Key_cols\n3:Seach Key_rows\n4:Search Super_keys"

def draw_state(stdscr, state_dict):
    '''Desenha gui na tela e atualiza os estados visiveis ao usuario'''

    state_dict['containers'] = dict()


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
    str_h_state_area_line = "+" + drawline(14) + "State area" + drawline(15)


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

