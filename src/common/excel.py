from src.utils import ExcelOperate

"""
封装自定义EXCEL操作
"""


class ExcelData(object):
    def __init__(self, file_path, sheet_name):
        self.operate_excel = ExcelOperate(file_path, sheet_name)

    def dict_data(self):
        rows = self.operate_excel.get_rows()  # 总行数
        cols = self.operate_excel.get_columns()  # 总列数
        head = self.get_head()  # 表头列表
        if rows > 1:
            reulst = []
            for i in range(2, rows):
                s = {}
                s['rowNum'] = i
                values = self.get_line_values(i)
                for x in range(cols):
                    s[head[x]] = values[x]
                reulst.append(s)
        else:
            raise ValueError('case数据为空，请检查')

        return reulst

    def get_head(self):
        """
        获取表头数据,第一行的数据
        """
        return self.operate_excel.get_row_values(0)

    def get_line_values(self, row_num):
        """
        获取一行的数据， 行号从1开始
        """
        return self.operate_excel.get_row_values(row_num-1)

    def result_write(self, row_num, value):
        """
        写入结果数据
        :param row_num: 行号从1开始
        :param value:  结果
        """
        self.operate_excel.write_value(row_num-1, 7, value)

    def copy_file(self, copy_to_path):
        """
        整个文件拷贝
        :param copy_to_path: 要拷贝到哪里
        """
        self.operate_excel.copy_file(copy_to_path)
