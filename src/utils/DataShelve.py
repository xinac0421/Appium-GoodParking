import shelve


class DataShelve(object):

    @staticmethod
    def shelve_write(path, key, value):
        """
        shelve数据存储
        :param path: shelve文件路径
        :param key: 键
        :param value: 值(可以是任何类型)
        :return: 如果成功则返回True
        """
        try:
            with shelve.open(path, flag='c', writeback=True) as write:  # 打开文件
                write[key] = value
            return True
        except IOError as e:
            return e

    @staticmethod
    def shelve_read(path, key):
        """
        shelve数据读取
        :param path: shelve文件路径
        :param key: 键
        :return: 返回值
        """
        with shelve.open(path, flag='c') as read:  # 打开文件
            value = read.get(key)
        return value



