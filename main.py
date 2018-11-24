#biblioteca de funcoes auxiliares contendo todas as outras bibliotecas. Ver codigo para mais detalhes
import aux_lib
from db import DB
from collections import defaultdict
import os

import easygui

#Curses para interface grafica
import curses

import sys

sys.setrecursionlimit(15000)

##Prefixo do local das tabelas fonte para a extração de dados
prefix_loc = "tabelas_mcti\\formatada\\2"


#Strings de menus e seus locais na tela em tuplas
str_menu_inicial = ("Select option:\n1:Generate database from tables\n2:Load database from object file\n0:Exit")
  

print(str_menu_inicial)
c = input()
os.system('cls')
f_exit = False



if c == '1':
    #Trie de testes
    teste = aux_lib.generate_table_trie(prefix_loc)
    db_teste = DB(teste)

elif c == '2':
    loc = easygui.fileopenbox("Select object file",filetypes = "*.obj")
    teste = aux_lib.load_trie(loc)
    db_teste = DB(teste)

else:
    f_exit = True


#################INICIALIZA REPL###################
#Inicializa estado da tela


#inicializa callable para ser wrapado
def main(stdscr):
    
    #flag que indica se é para sair do loop sair
    f_exit = False
    
    #sem eco
    #curses.noecho()
    
    #Sem enter para entrada
    curses.cbreak()

    #Dicionario de estados de tela#
    state_dict = defaultdict()
    
    #####Strings e respectivos locs#####



    #Local da linha de entrada de dados no programa
    loc_data_entry = (20,0)
    #move cursor para local de entrada de dados

    stdscr.move(loc_data_entry[0],loc_data_entry[1])

    while(f_exit == False):
        
        stdscr.refresh()
             
    #Encerra ao sair do loop   
    curses.endwin()

    
#Chama main
if(f_exit == False):
    stdscr = curses.initscr()
    curses.wrapper(main)




    


def write_stdscr(stdscr,string, loc):
    '''Write string in the stdscr using tuple loc(x,y) as x and y coordinates. Aligns new lines and restores cursor position after'''
    
    #Salvo local original do cursor
    loc_cursor = stdscr.getyx()

    #Separa por new lines    
    str_split = string.split('\n')
    counter = 0

    for line in str_split:

        stdscr.addstr(loc[0]+counter,loc[1],line)
        stdscr.refresh()
        counter += 1

    stdscr.move(loc_cursor[0],loc_cursor[1])


def write_stdscr_a(stdscr,string, loc, attrb):
    '''Write string in the stdscr using tuple loc(x,y) as x and y coordinates and attrb'''
    stdscr.addstr(loc[0],loc[1],string,attrb)





