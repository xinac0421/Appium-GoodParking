import time
import logging
from config.Constant import DEVICE_LIST_CONFIG_PATH, APP_INFO_CONFIG_PATH, ANDROID_APP_PATH
from src.utils.ConfigOperate import ConfigOperate
from appium import webdriver


class Driver:
    def __init__(self):
        self.device_cf = ConfigOperate(DEVICE_LIST_CONFIG_PATH)
        self.app = ConfigOperate(APP_INFO_CONFIG_PATH)
        self.log = logging.getLogger('main')

    def android_driver(self, device):
        port = self.device_cf.get_value(device, 'port')
        assert port is not None, 'port不能为空'
        # bport = self.device.get_value(device, 'bport')
        device = 'default' if device is None else device
        desired_caps = {
            'platformName': 'Android',
            'automationName': 'UiAutomator',
            'deviceName': str(device),
            'appPackage': self.app.get_value('app.info', 'package'),
            'appActivity': self.app.get_value('app.info', 'activity'),
            'noReset': False,
            'unicodeKeyboard': True,  # 编码,可解决中文输入问题
            'resetKeyboard': True,
            # 'autoAcceptAlerts': True,  # 默认选择接受弹窗条款  IOS独有，android不支持
            'app': ANDROID_APP_PATH,
            'noSign': True,  # 安装包不重新签名
            'newCommandTimeout': 30,
        }
        self.log.info('创建 %s 设备的driver, 连接端口为 %s 的appium服务......' % (device, port))
        driver = webdriver.Remote('http://127.0.0.1:%s/wd/hub' % port, desired_caps)
        self.log.info('连接成功')
        return driver
