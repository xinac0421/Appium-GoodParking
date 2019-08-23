
def screenshot(func):
    """
    截图装饰器：报错就截图
    """
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            import time
            import os
            import logging
            from config.Constant import IMAGE_DIR
            fun_name = func.__name__
            log = logging.getLogger('main.' + fun_name)
            nowtime = time.strftime("%Y-%m-%d_%H:%M:%S")
            device = self.driver.desired_capabilities.get('deviceName', None)  # 获取当前driver的deviceName参数的值
            file_name = 'default_%s_%s.png' % (fun_name, nowtime) if device is None else '%s_%s_%s.png' % (device, fun_name, nowtime)
            image_path = os.path.join(IMAGE_DIR, file_name)
            self.driver.save_screenshot(image_path)  # 截图
            log.error('%s测试失败: %s' % (fun_name, e))
    return wrapper
