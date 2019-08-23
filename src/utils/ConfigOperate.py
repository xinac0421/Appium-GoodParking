import configparser
import pathlib


class ConfigOperate:
    def __init__(self, file_path):
        self.cf = configparser.ConfigParser()
        self.file_path = file_path
        self.cf.read(file_path, encoding='utf-8-sig')

    def get_value(self, section, key):
        """
        获取配置文件里具体的值
        :param section: 节点
        :param key: 节点下的 键
        :return:  返回 值 ，找不到则返回None
        """
        return self.cf.get(section, key, fallback=None)  # 取不到返回None

    def get_key_value_dict(self, section):
        """
        获取 键值对的列表
        :param section: 节点
        :return: 返回 键值字典
        """
        try:
            items = self.cf.items(section)
            items_for_dict = {}
            for item in items:
                items_for_dict.update({item[0]: item[1]})
            return items_for_dict
        except configparser.NoSectionError:
            return None

    def get_sections(self):
        """
        显示所有节点列表
        :return: 节点列表
        """
        return self.cf.sections()

    def write_config(self, section, my_dict, is_clear=False):
        """
        配置写入(批量形式)
        :param section: 节点
        :param my_dict: 字典： {'a':'1','b':'2'}
        :param is_clear: 是否要清空再写入  默认False，即添加
        :return:
        """
        assert isinstance(my_dict, dict), '格式错误：my_dict需要为dict类型'
        if is_clear: self.cf.clear()
        if not self.cf.has_section(section):  # 如果section不存在则先添加section
            self.cf.add_section(section)
        for key, value in my_dict.items():
            self.cf.set(section, str(key), str(value))
        with open(self.file_path, 'w', encoding='utf-8') as f:
            self.cf.write(f)

    def write_config_for_value(self, section, key, value):
        """
        配置写入(单个)
        :param section:  节点
        :param key: 键
        :param value: 值
        :return:
        """
        if not self.cf.has_section(section):  # 如果section不存在则先添加section
            self.cf.add_section(section)
        self.cf.set(section, str(key), str(value))
        with open(self.file_path, 'w', encoding='utf-8') as f:
            self.cf.write(f)

    def clean(self):
        self.cf.clear()  # clear后还需要写入
        with open(self.file_path, 'w', encoding='utf-8') as f:
            self.cf.write(f)

    @staticmethod
    def file_is_exist(file_path):
        """
        文件是否存在
        :param file_path:  文件路径
        :return: 返回 True 和 False
        """
        path = pathlib.Path(file_path)
        if path.exists() and path.is_file():
            return True
        else:
            return False
