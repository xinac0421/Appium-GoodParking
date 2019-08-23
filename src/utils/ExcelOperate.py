import xlrd
from xlutils.copy import copy

"""
Excel基础操作类
"""


class ExcelOperate(object):
    def __init__(self, file_path, sheet_name):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.excel = self._get_all_excel()
        self.sheet_data = self._get_sheet_data(sheet_name)

    def _get_all_excel(self):
        """
        获取整个excel数据
        :return:
        """
        excel = xlrd.open_workbook(self.file_path)
        return excel

    def _get_sheet_data(self, sheet_name=0):
        """
        获取excel中的某个表数据
        :param sheet_name: 表名，可以是下标也可以是名称
        :return:
        """
        if isinstance(sheet_name, int):
            sheet = self.excel.sheet_by_index(sheet_name)
        else:
            sheet = self.excel.sheet_by_name(sheet_name)
        return sheet

    def get_rows(self):
        """
        获取excel行数
        :return:
        """

        return self.sheet_data.nrows

    def get_columns(self):
        """
        获取excel列数
        :return:
        """
        return self.sheet_data.ncols

    def get_cell_value(self, row, column):
        """
        获取单元格内容
        :param row:  行号
        :param column: 列号
        :return:
        """
        data = self.sheet_data.cell(row, column).value
        return data

    def get_row_values(self, row):
        """
        获取一行的数据
        :param row:
        """
        return self.sheet_data.row_values(row)

    def write_value(self, row, column, value):
        """
        数据写入
        :param row: 行
        :param column: 列
        :param value: 数据
        :return:
        """
        read_value = self.excel
        write_data = copy(read_value)
        write_save = write_data.get_sheet(self.sheet_name)
        write_save.write(row, column, value)
        write_data.save(self.file_path)

    def copy_file(self, copy_to_path):
        """
        整个文件拷贝
        :param copy_to_path: 要拷贝到哪里
        """
        read_value = self.excel
        write_data = copy(read_value)
        write_data.save(copy_to_path)




