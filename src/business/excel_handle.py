from config.Constant import APP_INFO_CONFIG_PATH
from src.utils import ConfigOperate
from src.common import KeyWords
import time
import logging
"""
excel与Appium集成操作类
需按固定的规则操作
"""


class ExcelHandle(object):
    def __init__(self, driver, data):
        self.driver = driver
        self.key_words = KeyWords(driver)
        self.cf = ConfigOperate(APP_INFO_CONFIG_PATH)
        self.log = logging.getLogger('main.' + __name__)

        self.handle_page = data.get('页面', None)
        self.handle_step = data.get('步骤', None)
        self.element_key = data.get('元素', None)
        self.handle_value = data.get('操作值', None)
        self.description = data.get('描述', None)

        self.step = {  # 执行步骤
            '输入': self._step_input,
            '点击': self._step_click,
            '左滑': self._step_swipe_left,
            '右滑': self._step_swipe_right,
            '上滑': self._step_swipe_up,
            '下滑': self._step_swipe_down,
            '验证元素存在': self._expect_has_element,
            '验证元素不存在': self._expect_has_not_element,
            '验证toast': self._get_toast,
            '等待': self._wait_second,
        }

    def run(self):
        self.log.info('开始执行用例: 页面-{ym},步骤-{bz},元素-{ys}{isczz}'.format(
            ym=self.handle_page,
            bz=self.handle_step,
            ys=self.element_key,
            isczz=',操作值-%s' % self.handle_value if self.handle_value else '')
        )
        step_fun = self.step.get(self.handle_step, None)  # 获取操作函数名
        if step_fun is None:
            message = '没有找到步骤为"%s"的操作代码！' % self.handle_step
            self.log.error(message)
            raise ValueError(message)
        return step_fun()  # 运行函数，加上括号表示函数，才会运行

    def _get_locator(self):
        """通过页面和元素名称获取 本地App.ini文件里的loc """
        if self.handle_page and self.element_key:
            loc = self.cf.get_value(self.handle_page, self.element_key)
            if loc is None:
                message = '自定义元素没有找到: handle_page=%s, element_key=%s' % (self.handle_page, self.element_key)
                self.log.error(message)
                raise ValueError(message)
            return loc
        else:
            message = '页面和步骤不能为空'
            self.log.error(message)
            raise ValueError(message)

    def _step_input(self):
        """操作:输入信息"""
        if self.handle_value:
            self.key_words.input_text(self._get_locator(), self.handle_value)
        else:
            message = '当步骤为"输入"时,操作值不能为空！'
            self.log.error(message)
            raise ValueError(message)
        return 'PASS'

    def _step_click(self):
        """操作：点击"""
        self.key_words.click_element(self._get_locator())
        return 'PASS'

    def _step_swipe_left(self):
        """操作:左滑"""
        self.key_words.swipe_left()
        return 'PASS'

    def _step_swipe_right(self):
        """操作:右滑"""
        self.key_words.swipe_right()
        return 'PASS'

    def _step_swipe_up(self):
        """操作:上滑"""
        self.key_words.swipe_up()
        return 'PASS'

    def _step_swipe_down(self):
        """操作:下滑"""
        self.key_words.swipe_down()
        return 'PASS'

    def _wait_second(self):
        """等待"""
        try:
            if self.handle_value:
                time.sleep(int(self.handle_value))
            else:
                message = '当步骤为"等待"时,操作值不能为空！'
                self.log.error(message)
                raise ValueError(message)
        except ValueError as e:
            return e
        return 'PASS'


#   ------------以下为预期结果验证操作，均有返回值----------------------
    def _expect_has_element(self):
        """验证元素存在"""
        if self.element_key:
            result = self.key_words.isElement(self._get_locator())
            return 'PASS' if result is True else 'ERROR: 元素不存在'
        else:
            message = '当步骤为"验证元素存在"时,元素不能为空！'
            self.log.error(message)
            raise ValueError(message)

    def _expect_has_not_element(self):
        """验证元素不存在"""
        if self.element_key:
            result = self.key_words.isElement(self._get_locator())
            return 'PASS' if result is False else 'ERROR: 预期元素仍旧存在'
        else:
            message = '当步骤为"验证元素不存在"时,预期元素不能为空！'
            self.log.error(message)
            raise ValueError(message)

    def _get_toast(self):
        """验证toast字符"""
        if self.handle_value:
            text = self.key_words.get_toast(self.handle_value)
            return 'PASS' if text else 'ERROR: toast字符没有找到'
        else:
            message = '当步骤为"验证toast"时,操作值不能为空！'
            self.log.error(message)
            raise ValueError(message)
