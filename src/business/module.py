from config.Constant import APP_INFO_CONFIG_PATH
from src.utils import ConfigOperate
from src.common import KeyWords
import time
import logging


class Module(object):
    def __init__(self, driver):
        self.key_words = KeyWords(driver)
        self.driver = driver
        self.cf = ConfigOperate(APP_INFO_CONFIG_PATH)
        self.log = logging.getLogger('main.' + __name__)

    def start_page_or_home(self):
        """
        判断是否已到首页，如果在启动页则先做进入首页操作
        """
        if self.key_words.isElement(self.cf.get_value('首页', '启动图')):
            self.log.info('存在启动页，开始做左滑并进入首页操作')
            self.key_words.swipe_left()
            self.key_words.swipe_left()
            self.key_words.swipe_left()
            self.key_words.click_element(self.cf.get_value('首页', '启动图的立即体验按钮'))
        self.driver.implicitly_wait(5)

    def is_allow_frame_close(self):
        """
        启动的时候如果有权限弹框，则点击允许
        """
        for i in range(3):
            self.log.info('检查是否存在权限弹框')
            if self.key_words.isElement(self.cf.get_value('首页', '权限提示框')):
                self.log.info('存在权限弹框，点击"允许"按钮')
                self.key_words.click_element(self.cf.get_value('首页', '权限提示框'))
            time.sleep(1)

    def is_update_frame_close(self):
        """首页若有更新弹窗，则点击关闭"""
        self.log.info('检查是否存在更新提示弹窗')
        if self.key_words.isElement(self.cf.get_value('首页', '更新弹窗')):
            self.log.info('存在更新提示弹窗，点击"以后再说"按钮')
            self.key_words.click_element(self.cf.get_value('首页', '更新弹窗取消按钮'))
        time.sleep(1)


    def back_to_home(self):
        """
        返回到首页
        :return:
        """
        self.log.info('开始做返回到首页操作')
        for i in range(5):
            if not self.key_words.isElement(self.cf.get_value('首页', '首页我的头像按钮')):
                self.driver.back()
                self.driver.implicitly_wait(2)

    def is_login(self):
        """
        判断是否已登录
        :return:
        """
        self.back_to_home()
        self.key_words.click_element(self.cf.get_value('首页', '首页我的头像按钮'))
        self.driver.implicitly_wait(2)
        loc_nickname = self.cf.get_value('个人中心', '昵称')  # 获取昵称元素
        if self.key_words.isElement(loc_nickname):
            return True
        else:
            return False
