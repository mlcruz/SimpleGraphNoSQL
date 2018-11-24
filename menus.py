#Arquivos contendo os menus do programa. Cada menu recebe um strscr e um dicionario de estados, e os gerencia conforme a necessidade.

import curses
import aux_lib
import easygui

from db import DB
from collections import defaultdict
import os


from aux_lib import write_stdscr, write_stdscr_a

def menu_inicial(state_dict):

    #Strings de menus e seus locais na tela em tuplas
    str_menu_inicial = "Select option:\n1:Generate database from tables\n2:Load database from object file\n0:Exit"

    print(str_menu_inicial)
    c = input()
    os.system('cls')
    f_exit = False



    if c == '1':
        #Trie de tabelas
        state_dict['table_trie'] = aux_lib.generate_table_trie(prefix_loc)
        state_dict['databease'] = DB(teste)

    elif c == '2':
        state_dict['loc'] = easygui.fileopenbox("Select object file",filetypes = "*.obj")
        teste = aux_lib.load_trie(state_dict['loc'])
        state_dict['db'] = DB(teste)

    else:
        state_dict['f_exit'] = True
