#biblioteca de funcoes auxiliares contendo todas as outras bibliotecas. Ver codigo para mais detalhes
import aux_lib



class DB(object):
    '''Cria banco de dados a partir de uma trie de tabelas'''

    def __init__(self, trie):
        '''Inicialize banco de dados com uma trie recebida'''

        #Cria trie de chaves
        key_row_trie = aux_lib.Trie()

        #Insere colunas ordenadores nas tries de chaves
        for label,table in trie.strings_dict.items():
            for X in range(table.bound_x):
                for Y in range(table.bound_y):
                    cell = table.table_data[X][Y]
                    #Insere somente celulas do tipo key_row
                    if cell.cell_type == "Key_Row":
                        aux_lib.insert(cell.cell_name,cell.child_nodes,key_row_trie.root)

        #cria dicionario de strings da trie de colunas chave
        key_row_trie.yield_strings(key_row_trie.root)

        #Gera trie reversa
        aux_lib.generate_reverse_trie(key_row_trie)


            








