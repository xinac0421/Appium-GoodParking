import time
import os
from src.utils import Tools

"""
这里做一些常量的设置
"""

# 日志等级
LOG_LEVEL = 'DEBUG'   # DEBUG,INFO

# APP所有信息配置文件路径
APP_INFO_CONFIG_PATH = os.path.join(Tools.get_project_dir(), 'config', "App.ini")


# 设备列表配置文件路径
DEVICE_LIST_CONFIG_PATH = os.path.join(Tools.get_project_dir(), 'config', "device.ini")

#  APP安装包路径
ANDROID_APP_PATH = os.path.join(Tools.get_project_dir(), 'config', 'GoodParking2.7.4.apk')

# 图片保存路径
IMAGE_DIR = os.path.join(Tools.get_project_dir(), 'logs', 'device', 'image')

# excel_base.xls文件路径
EXCEL_BASE_PATH = os.path.join(Tools.get_project_dir(), 'src', 'testcase', 'case_base.xls')

# excel运行结果保存路径
EXCEL_RESULT_DIR = os.path.join(Tools.get_project_dir(), 'src', 'testcase', 'result')


# 获取日志路径
def get_log_path(device_name):
    date = time.strftime("%Y-%m-%d")
    path = os.path.join(Tools.get_project_dir(), 'logs', 'device', '%s_%s.log' % (device_name, date))
    return path
