#Arquivos contendo os menus do programa. Cada menu recebe um strscr e um dicionario de estados, e os gerencia conforme a necessidade.

import curses
import aux_lib
import easygui

from db import DB
from collections import defaultdict
import os


from aux_lib import write_stdscr, write_stdscr_a



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
    loc_saving = (8,0)

    str_done = "Done\n"
    loc_done = (10,0)


    #escreve menu na tela
    write_stdscr(stdscr,str_menu_inicial,loc_menu_inicial)

    #Controle de loop
    local_exit = False

    #loop de repl local
    while(local_exit == False):
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

    #Linha separando input do usuario
    str_user_input_line = drawline(52) + "User Input Area" + drawline(52)
    loc_user_input_line = (35,0)

    #Linha seperando area de estados
    str_state_area_line = drawbar(35) + "+"
    loc_state_area_line = (0,80)

    write_stdscr(stdscr,str_user_input_line,loc_user_input_line)
    write_stdscr(stdscr,str_state_area_line,loc_state_area_line)





def drawline(intr):
    '''Returns the '-' char repeated 9 times in a string'''
    returns = ''
    for x in range(intr):
        returns = returns + '-'
    return returns

def drawbar(intr):
    '''Returns the '-' char repeated 9 times in a string'''
    returns = ''
    for x in range(intr):
        returns = returns + '|\n'
    return returns

