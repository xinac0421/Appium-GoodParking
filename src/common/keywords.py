"""
公共关键字
"""
from ._elementfinder import ElementFinder
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import logging


class KeyWords:
    # 初始化
    def __init__(self, driver):
        self.driver = driver
        self._element_finder = ElementFinder()
        self.log = logging.getLogger('main.keywords')  # 继承日志设置

    def isElement(self, locator):
        """
        元素是否存在
        :param self:
        :param locator: 自定义元素
        :return: bool类型
        """
        flag = False
        try:
            self._element_finder.find(self.driver, locator)
            flag = True
        except NoSuchElementException:
            flag = False
        except TimeoutException:
            flag = False
        finally:
            return flag

    def click_element(self, locator):
        """
        封装点击元素操作
        :param locator: 自定义元素
        :return:
        """
        self._element_finder.find(self.driver, locator).click()

    def input_text(self, locator, text):
        """
        输入文本
        :param locator: 元素
        :param text: 文本
        :return:
        """
        self._element_finder.find(self.driver, locator).send_keys(text)

    def swipe_left(self, duration=1000):
        """
        封装滑动方法(按比例往左滑动)
        :param duration: 时间
        :return:
        """
        try:
            self._swipe_by_percent(80, 50, 20, 50, duration)
        except Exception as e:
            self.log.error('滑动屏幕出错'.format(e))

    def swipe_right(self, duration=1000):
        """
        封装滑动方法(按比例往右滑动)
        :param duration: 时间
        :return:
        """
        try:
            self._swipe_by_percent(20, 50, 80, 50, duration)
        except Exception as e:
            self.log.error('滑动屏幕出错'.format(e))

    def swipe_up(self, duration=1000):
        """
        封装滑动方法(按比例往上滑动)
        :param duration: 时间
        :return:
        """
        try:
            self._swipe_by_percent(50, 80, 50, 20, duration)
        except Exception as e:
            self.log.error('滑动屏幕出错'.format(e))

    def swipe_down(self, duration=1000):
        """
        封装滑动方法(按比例往上滑动)
        :param duration: 时间
        :return:
        """
        try:
            self._swipe_by_percent(50, 20, 50, 80, duration)
        except Exception as e:
            self.log.error('滑动屏幕出错'.format(e))

    def get_toast(self, text):
        """
        获取toast字符('automationName'必须为'UiAutomator2')
        :param text: toast字符
        :return:
        """
        toast_loc = ('xpath', '//*[contains(@test, %s)]' % text)
        e1 = WebDriverWait(self.driver, 10, 0.2).until(expected_conditions.presence_of_element_located(toast_loc))
        return e1.text

    def _get_current(self):
        """
        获取当前Android活动的名称
        :param self:
        :return:
        """
        return self.driver.current_activity


    def _get_platform(self):
        """
        获取当前运行的设备是ios还是android
        :param self:
        :return: 返回 ios或者android
        """
        platform_name = self.driver.desired_capabilities['platformName']
        return platform_name.lower()

    def _swipe_by_percent(self, start_x, start_y, end_x, end_y, duration=1000):
        """
        按百分比滑动，从屏幕的百分比滑动到另一个百分比，时间参数可选。
        普通滑动无法针对不同的屏幕分辨率进行缩放。

        参数:
            - start_x - x-percent at which to start
            - start_y - y-percent at which to start
            - end_x - x-percent distance from start_x at which to stop
            - end_y - y-percent distance from start_y at which to stop
            - duration - (optional) time to take the swipe, in ms.

        注：这也考虑了iOS和Android之间不同的滑动行为。代码参考了robot_framework的AppiumLibrary

        """
        size = self.driver.get_window_size()
        width = size['width']
        height = size['height']
        x_start = round(float(start_x) / 100 * width)
        x_end = round(float(end_x) / 100 * width)
        y_start = round(float(start_y) / 100 * height)
        y_end = round(float(end_y) / 100 * height)
        x_offset = round(x_end - x_start)
        y_offset = round(y_end - y_start)
        platform = self._get_platform()
        if platform == 'android':
            self.driver.swipe(x_start, y_start, x_end, y_end, duration)
        else:
            self.driver.swipe(x_start, y_start, x_offset, y_offset, duration)









