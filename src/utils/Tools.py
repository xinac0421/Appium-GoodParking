import subprocess
import time
import os


class Tools(object):
    @staticmethod
    def getreqtime():
        """获取当前的13位的时间戳
         | getreqtime |
        """
        return str(int(time.time()*1000))  # 13位时间戳，与java里一致

    @staticmethod
    def get_now_date(form='%Y-%m-%d %H:%M:%S'):
        """
        获取当前的时间(年-月-日 时:分:秒)
        :return:返回时间
        """
        return time.strftime(form)


    @staticmethod
    def get_project_dir():
        """
        以Tools该文件路径为基础,获取项目路径
        :return:返回项目根目录路径
        """
        project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return project_dir

    @staticmethod
    def get_plate_keyboard_position(left_x, left_y, width, height, value):
        """获取字符所在的位置(坐标),该方法只对CT3.0_APP的车牌绑定界面里车牌号输入框的键盘有效
            left_x:左上 x 坐标
            left_y:左上 y 坐标
            width: 键盘的宽
            height: 键盘的高
            str: 查询的字符
        | get_plate_keyboard_osition | left_x | left_y | width | height | str |
                :return:返回字符的坐标
        """
        left_x = float(left_x)
        left_y = float(left_y)
        width = float(width)
        height = float(height)
        x_jg = round(width/10, 1)
        y_jg = round(height/5, 1)
        two_row_height = round(left_y + y_jg * 1.5, 1)
        three_row_height = round(left_y + y_jg * 2.5, 1)
        four_row_height = round(left_y + y_jg * 3.5, 1)
        five_row_height = round(left_y + y_jg * 4.5, 1)
        left_A_x = left_x + x_jg * 0.5
        left_Z_x = left_x + x_jg * 1.5
        d = {'1': (round(left_x + x_jg * 0.5, 1), two_row_height),
             '2': (round(left_x + x_jg * 1.5, 1), two_row_height),
             '3': (round(left_x + x_jg * 2.5, 1), two_row_height),
             '4': (round(left_x + x_jg * 3.5, 1), two_row_height),
             '5': (round(left_x + x_jg * 4.5, 1), two_row_height),
             '6': (round(left_x + x_jg * 5.5, 1), two_row_height),
             '7': (round(left_x + x_jg * 6.5, 1), two_row_height),
             '8': (round(left_x + x_jg * 7.5, 1), two_row_height),
             '9': (round(left_x + x_jg * 8.5, 1), two_row_height),
             '0': (round(left_x + x_jg * 9.5, 1), two_row_height),
             'Q': (round(left_x + x_jg * 0.5, 1), three_row_height),
             'W': (round(left_x + x_jg * 1.5, 1), three_row_height),
             'E': (round(left_x + x_jg * 2.5, 1), three_row_height),
             'R': (round(left_x + x_jg * 3.5, 1), three_row_height),
             'T': (round(left_x + x_jg * 4.5, 1), three_row_height),
             'Y': (round(left_x + x_jg * 5.5, 1), three_row_height),
             'U': (round(left_x + x_jg * 6.5, 1), three_row_height),
             'I': (round(left_x + x_jg * 7.5, 1), three_row_height),
             'O': (round(left_x + x_jg * 8.5, 1), three_row_height),
             'P': (round(left_x + x_jg * 9.5, 1), three_row_height),
             'A': (round(left_A_x + x_jg * 0.5, 1), four_row_height),
             'S': (round(left_A_x + x_jg * 1.5, 1), four_row_height),
             'D': (round(left_A_x + x_jg * 2.5, 1), four_row_height),
             'F': (round(left_A_x + x_jg * 3.5, 1), four_row_height),
             'G': (round(left_A_x + x_jg * 4.5, 1), four_row_height),
             'H': (round(left_A_x + x_jg * 5.5, 1), four_row_height),
             'J': (round(left_A_x + x_jg * 6.5, 1), four_row_height),
             'K': (round(left_A_x + x_jg * 7.5, 1), four_row_height),
             'L': (round(left_A_x + x_jg * 8.5, 1), four_row_height),
             'Z': (round(left_Z_x + x_jg * 0.5, 1), five_row_height),
             'X': (round(left_Z_x + x_jg * 1.5, 1), five_row_height),
             'C': (round(left_Z_x + x_jg * 2.5, 1), five_row_height),
             'V': (round(left_Z_x + x_jg * 3.5, 1), five_row_height),
             'B': (round(left_Z_x + x_jg * 4.5, 1), five_row_height),
             'N': (round(left_Z_x + x_jg * 5.5, 1), five_row_height),
             'M': (round(left_Z_x + x_jg * 6.5, 1), five_row_height),
             }
        value = str(value)
        return d[value]

    @staticmethod
    def run_server(command, server_log_path=None):
        """
        创建子进程运行appium的server
        :param command: 命令参数,str类型
        :param server_log_path: 是否要把server日志(这里主要指appium服务)存入文件,默认为None为不存,不存则会实时输出到控制台
        :return:返回subprocess子进程对象
        """
        if server_log_path:
            file_out = open(server_log_path, 'w+', encoding='utf-8')
            child = subprocess.Popen(command, stdout=file_out, shell=True)
        else:
            child = subprocess.Popen(command, shell=True)

        #child.wait()
        return child

    @staticmethod
    def stop_server(child):
        """  停止appium的server,需传入subprocess子进程对象"""
        child.terminate()
        print('服务已停止')

    @staticmethod
    def adb_install_apk(device_serial, app_path):
        """
        用adb命令的形式安装apk,且权限全开(经测试,权限属性没用)
        :param app_path: apk安装包的路径
        :param device_serial:指定安装的设备序列号
        :return:
        """
        comm = 'adb -s {0} install -r -g {1}'.format(device_serial, app_path)
        subprocess.run(comm, check=True, shell=True)
