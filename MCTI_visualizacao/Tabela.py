#xlrd é uma biblioteca para facilitar o parsing de tabelas xls do excel
import xlrd

class Tabela(object):
    """Classe que representa uma tabela"""

    def __init__(self, loc):
        """Inicializa uma tabela a partir de um local loc"""

        self.loc_source = loc

        #Tabela original como xls, parseada pelo xlrd
        self.raw_table = xlrd.open_workbook(loc,formatting_info=True)

        #Folha da tabela original
        self.raw_sheet = self.raw_table.sheet_by_index(0)

        #Label da tabela, primeira coluna primeira linha
        self.table_label = self.raw_sheet.cell_value(rowx=0, colx=0)







