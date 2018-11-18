#Lista diretorios
from os import listdir

##Biblioteca com funções auxiliares para o trabalho

#Gerador para numeros de tabelas
def generate_num(tab_loc):
    '''Gera o nome do arquivo de tabela a cada passo'''
    
    index = 0
    
    #lista com todos os nomes das tabelas
    tables = listdir(tab_loc)
    l_tab = len(tables)

    while (index < l_tab):
        
        yield tables[index]
        index = index + 1

    return 0

#Gerador para locais de tabela a partir da pasta fonte da tabelas
def generate_loc(tab_loc):
    """Gera o local da tabela a cada passo"""
    
    tabs = generate_num(tab_loc)
    loc = tab_loc+"\\"
    get = next(tabs)
    

    while(get != 0):
        yield loc+get
        get = next(tabs)


    


    



    








