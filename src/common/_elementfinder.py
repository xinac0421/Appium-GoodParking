"""
封装一些查找元素操作
"""


class ElementFinder(object):
    # 初始化
    def __init__(self):
        self._strategies = {
            'id': self._find_by_id,
            'xpath': self._find_by_xpath,
            'class': self._find_by_class_name,
            'accessibility_id': self._find_element_by_accessibility_id,
            'android': self._find_by_android,
            'ios': self._find_by_ios,
            'css': self._find_by_css_selector,
            'jquery': self._find_by_sizzle_selector,
        }

    def find(self, driver, locator):
        assert driver is not None
        assert locator is not None and len(locator) > 0

        (prefix, criteria) = self._parse_locator(locator)
        prefix = 'default' if prefix is None else prefix
        strategy = self._strategies.get(prefix)
        if strategy is None:
            raise ValueError("Element locator with prefix '" + prefix + "' is not supported")
        return strategy(driver, criteria)

    def _parse_locator(self, locator):
        """
        分割自定义元素形式:id=xxxx
        :param locator: 自定义格式的元素
        :return: 返回分割后的字符'id','xxxx'
        """
        prefix = None
        criteria = locator
        if not locator.startswith('//'):
            locator_parts = locator.partition('=')
            if len(locator_parts[1]) > 0:
                prefix = locator_parts[0].strip().lower()
                criteria = locator_parts[2].strip()
        return prefix, criteria

    def _find_by_id(self, driver, criteria):
        return driver.find_element_by_id(criteria)

    def _find_by_name(self, driver, criteria):
        return driver.find_element_by_name(criteria)

    def _find_by_xpath(self, driver, criteria):
        return driver.find_element_by_xpath(criteria)

    def _find_by_class_name(self, driver, criteria):
        return driver.find_element_by_class_name(criteria)

    def _find_by_android(self, driver, criteria):  # new UiSelector()
        return driver.find_element_by_android_uiautomator(criteria)

    def _find_by_ios(self, driver, criteria):  # new UiSelector()
        return driver.find_element_by_ios_uiautomation(criteria)

    def _find_element_by_accessibility_id(self, driver, criteria):
        return driver.find_element_by_accessibility_id(criteria)

    def _find_by_css_selector(self, driver, criteria):
        return driver.find_elements_by_css_selector(criteria)

    def _find_by_sizzle_selector(self, driver, criteria):
        js = "return jQuery('%s').get();" % criteria.replace("'", "\\'")
        return driver.execute_script(js)




