#biblioteca de funcoes auxiliares contendo todas as outras bibliotecas. Ver codigo para mais detalhes
import aux_lib



class DB(object):
    '''Cria banco de dados a partir de uma trie de tabelas'''

    def __init__(self, trie):
        '''Inicialize banco de dados com uma trie recebida'''

        self.tables = trie

        #Cria trie de linhas chaves
        self.key_rows = aux_lib.Trie()

        #Cria trie de colunas chaves
        self.key_cols = aux_lib.Trie()

        #Cria trie de super chaves
        self.super_key = aux_lib.Trie()

        #Insere colunas ordenadores nas tries de chaves
        for label,table in trie.strings_dict.items():
            for X in range(table.bound_x):
                for Y in range(table.bound_y):
                    #Celula atual
                    cell = table.table_data[X][Y]

                    #Insere celulas do tipo Key_row na trie especificada
                    if cell.cell_type == "Key_Row":
                        aux_lib.insert(cell.cell_name,cell.child_nodes,self.key_rows.root)

                    #Insere celulas do tipo Key_Col na trie especificada
                    if cell.cell_type == "Key_Col":
                        aux_lib.insert(cell.cell_name,cell.child_nodes,self.key_cols.root)

                    if cell.cell_type == "Super_Key":
                        aux_lib.insert(cell.cell_name,cell.child_nodes,self.super_key.root)



        #cria dicionario de strings da trie de colunas chave
        self.key_rows.yield_strings(self.key_rows.root)
        self.key_cols.yield_strings(self.key_cols.root)
        self.super_key.yield_strings(self.super_key.root)

        #Gera trie reversa da trie de colunas e linhas chaves
        aux_lib.generate_reverse_trie(self.key_rows)
        aux_lib.generate_reverse_trie(self.key_cols)
        aux_lib.generate_reverse_trie(self.super_key)




            








