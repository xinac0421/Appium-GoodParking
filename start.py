import os
import sys
rootPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(rootPath)
import multiprocessing
import time
import unittest
import ddt
from src.common.driver import Driver
from src.common.server import Server
from src.utils import ConfigOperate
from src.utils import HTMLTestRunner
from config.Constant import DEVICE_LIST_CONFIG_PATH, get_log_path, EXCEL_BASE_PATH, EXCEL_RESULT_DIR
from src.utils import Logging
from src.utils.wrappers import screenshot
from src.common.excel import ExcelData
from src.business.excel_handle import ExcelHandle
from src.business.module import Module


@ddt.ddt
class CaseTests(unittest.TestCase):
    def __init__(self, methodName='runTest', param=None):
        super(CaseTests, self).__init__(methodName)
        self.now = time.strftime("%Y-%m-%d %H_%M_%S")
        ExcelData(EXCEL_BASE_PATH, sheet_name=0).copy_file(os.path.join(EXCEL_RESULT_DIR, 'case_result_%s.xls' % self.now))
        global device
        device = param

    @staticmethod
    def parametrize(testcase_klass, param=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param))
        return suite

    @classmethod
    @screenshot
    def setUpClass(cls):
        Logging(get_log_path(device))
        print('this is setUpClass')
        cls.driver = Driver().android_driver(device)
        cls.driver.implicitly_wait(5)
        cls.md = Module(cls.driver)
        cls.md.start_page_or_home()
        cls.md.is_allow_frame_close()
        cls.md.is_update_frame_close()

    @classmethod
    def tearDownClass(cls):
        time.sleep(5)
        cls.driver.quit()

    def setUp(self):
        print("this is setup\n")

    def tearDown(self):
        time.sleep(1)
        print("this is teardown\n")

    @ddt.data(*ExcelData(EXCEL_BASE_PATH, sheet_name=0).dict_data())
    @screenshot
    def test_excel(self, data):
        run_result = ExcelHandle(self.driver, data).run()
        # 把结果保存到result文件夹里
        excel_op = ExcelData(os.path.join(EXCEL_RESULT_DIR, 'case_result_%s.xls' % self.now), sheet_name=0)
        excel_op.result_write(data['rowNum'], run_result)
        self.assertEqual(run_result, 'PASS')


def start(device):
    suite = unittest.TestSuite()
    suite.addTest(CaseTests.parametrize(CaseTests, param=device))
    unittest.TextTestRunner(verbosity=2).run(suite)

    """
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = './report/' + device + '_' + now + '_result.html'
    fp = open(filename, 'wb')
    try:
        HTMLTestRunner(stream=fp,
                   title='好停车测试报告',
                   description='描述信息？'
                   ).run(suite)
    except Exception as e:
        print(e)
    finally:
        fp.close()
    """
#Server().main()  # 启动Appium服务
#time.sleep(10)

if __name__ == '__main__':
    cf = ConfigOperate(DEVICE_LIST_CONFIG_PATH)
    section_list = cf.get_sections()
    server = Server()
    # 先尝试停掉上次运行后的僵尸appium服务
    for section in section_list:
        port = cf.get_value(section, 'port')
        bport = cf.get_value(section, 'bport')
        for p in [port, bport]:
            server.kill_server(p)
            time.sleep(2)

    server.main()  # 启动Appium服务
    time.sleep(10)  # 加个时间等待服务先启动

    process = []
    for device in section_list:
        p = multiprocessing.Process(target=start, args=(device,))
        p.start()
        process.append(p)
    for p in process:
        p.join()  # 等待所有进程执行完毕



