#biblioteca de funcoes auxiliares contendo todas as outras bibliotecas. Ver codigo para mais detalhes
import aux_lib

import menus
from menus import Container
import sys

from collections import defaultdict

import curses

sys.setrecursionlimit(15000)

##Prefixo do local das tabelas fonte para a extração de dados
prefix_loc = "tabelas_mcti\\formatada\\2"

#Cria dicionario de estados
state_dict = defaultdict()


#Indica se deve sair do loop
state_dict['f_exit'] = False
state_dict['state'] = 'start_menu'


#Inicializa banco de dados e seus estados
menus.start_menu(state_dict)


#################INICIALIZA REPL###################

#inicializa callable para ser wrapado
def main(stdscr,state_dict):

    #Sem enter para entrada
    
    
  
    #Local da linha de entrada de dados no programa
    state_dict['loc_data_entry'] = (52,0)
    #move cursor para local de entrada de dados

    stdscr.move((state_dict['loc_data_entry'])[0],(state_dict['loc_data_entry'])[1])

    while(state_dict['f_exit'] == False):
        
        menus.main_menu(stdscr,state_dict)



        #Fim dos menus de estado
        #stdscr.getch()
       
             
    #Encerra ao sair do loop   
    

    
#Chama main
if(state_dict['f_exit'] == False):
    #Inicializa estado da tela
    stdscr = curses.initscr()
    curses.resize_term(55,160)
    try :
        curses.wrapper(main(stdscr,state_dict))
    except:
        menus.os.system('cls')
        print("fim")





