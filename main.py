#biblioteca de funcoes auxiliares contendo todas as outras bibliotecas. Ver codigo para mais detalhes
import aux_lib

import menus
import sys

from collections import defaultdict

import curses

sys.setrecursionlimit(15000)

##Prefixo do local das tabelas fonte para a extração de dados
prefix_loc = "tabelas_mcti\\formatada\\2"

state_dict = defaultdict()

#Indica se deve sair do loop
state_dict['f_exit'] = False

menus.menu_inicial(state_dict)


#################INICIALIZA REPL###################
#Inicializa estado da tela

#inicializa callable para ser wrapado
def main(stdscr,state_dict):

    #Sem enter para entrada
    curses.cbreak()
    
    #####Strings e respectivos locs e estados possiveis#####
    str_menu_inicial = "9:Save Current DB\n0:Exit"
    loc_menu_inicial = (0,0)



    #Local da linha de entrada de dados no programa
    loc_data_entry = (20,0)
    #move cursor para local de entrada de dados

    stdscr.move(loc_data_entry[0],loc_data_entry[1])

    while(state_dict['f_exit'] == False):
        
        c = stdscr.getkey()
        stdscr.refresh()
             
    #Encerra ao sair do loop   
    curses.endwin()

    
#Chama main
if(state_dict['f_exit'] == False):
    stdscr = curses.initscr()
    curses.wrapper(main(stdscr,state_dict))





