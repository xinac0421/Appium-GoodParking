import subprocess
import platform
import multiprocessing
import os
from src.utils.ConfigOperate import ConfigOperate
from src.utils.Tools import Tools
from src.utils import Logging


class Server(object):
    def __init__(self):
        self.project_dir = Tools.get_project_dir()
        device_config_path = self.project_dir + '/config/device.ini'
        self.cf = ConfigOperate(device_config_path)

    def main(self, device_list=None):
        """
        多线程启动appium server主程序
        :param device_list: 设备列表
        :return:
        """
        if device_list is None:  # 如果设备列表没有传进来，则自动去当前系统里去获取
            device_list = self._get_android_devices()  # 获取安卓设备列表
        if device_list:
            appium_port_list = self._create_port_list(4700, len(device_list))
            bootstrap_port_list = self._create_port_list(4900, len(device_list))
            self.cf.clean()  # 先清空device配置文件
            for i in range(len(device_list)):
                port = appium_port_list[i]
                bport = bootstrap_port_list[i]
                device = device_list[i]
                server_log_path = os.path.join(Tools.get_project_dir(), 'logs', 'servers', '%s_%s.log' % (device, Tools.get_now_date('%Y-%m-%d_%H:%M:%S')))
                self.cf.write_config(device, {'port': port, 'bport': bport, 'server_log_path': server_log_path})  # 把设备信息和端口信息写入配置文件
                t = multiprocessing.Process(target=self.start_server, args=(port, bport, device, server_log_path))
                t.daemon = True  # 设置为守护进程，且一定要在t.start()前设置,设置t为守护进程,禁止t创建子进程,并且父进程代码执行结束,t即终止运行
                t.start()
        else:
            raise ValueError('当前没有任何连接设备')

    def start_server(self, port, bport, device, log_path=None):
        """
        创建子进程运行appium的server
        :param port: 端口
        :param bport: b端口
        :param device:  设备名
        :param log_path: log路径
        """
        if log_path:
            command = 'appium -p {port} --bootstrap-port {bport} -U {device} --log {log_path} ' \
                      '--local-timezone --session-override'.format(
                port=port, bport=bport, device=device, log_path=log_path)
        else:
            command = 'appium -p {port} --bootstrap-port {bport} -U {device} ' \
                      '--local-timezone --session-override'.format(
                port=port, bport=bport, device=device)

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if len(result.stderr) > 0:
            message = '--------启动port端口为%s，bport端口为%s，设备uuid为%s的appium服务失败！！！---------\n' \
                      'error_message:%s' % (port, bport, device, result.stderr)
        else:
            message = '--------启动port端口为%s，bport端口为%s，设备uuid为%s的appium服务成功！！！---------\n' \
                      % (port, bport, device)
        Logging().info(message)


    def kill_server(self, port):
        """
        停止服务
        :param port: 传入服务的端口
        :return: 返回 message
        """
        system = platform.system()
        if system == 'Darwin':  # MAC 系统
            ms = subprocess.Popen(['lsof', '-i:%s' % port], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            lines = ms.stdout.readlines()
            if len(lines) > 0:
                lines = lines[1:]
                pid_list = []
                for line in lines:
                    lline = line.strip().split()
                    pid_list.append(bytes(lline[1]).decode())
                message = '端口%s被占用的pid有：%s' % (port, pid_list) + \
                          '\n---------------开始执行清理程序————————————————'
                Logging().info(message)
                for pid in pid_list:
                    subprocess.run(['kill', '-9', str(pid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if self._port_is_used(port):
                    message = '---------------端口 %s 仍旧被占用，程序清理失败，请检查————————————————' % port
                    Logging().info(message)
                else:
                    message = '---------------端口 %s 清理成功！————————————————' % port
                    Logging().info(message)
            else:
                message = '---------------端口 %s 未被占用，无需清理----------' % port
                Logging().info(message)

        elif system == 'Windows':  # Windows 系统
            p1 = subprocess.Popen(['netstat', '-ano'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ws = subprocess.Popen(['findstr', str(port)], stdin=p1.stdout, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            lines = ws.stdout.readlines()
            if len(lines) > 0:
                pid_list = []
                for line in lines:
                    lline = line.strip().split()
                    pid_list.append(bytes(lline[-1]).decode())
                message = '端口%s被占用的pid有：%s' % (port, pid_list) + \
                          '\n---------------开始执行清理程序————————————————'
                Logging().info(message)
                for pid in pid_list:
                    subprocess.run('taskkill -f -pid %s' % pid, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                if self._port_is_used(port):
                    message = '---------------端口 %s 仍旧被占用，程序清理失败，请检查————————————————' % port
                    Logging().info(message)
                else:
                    message = '---------------端口 %s 清理成功！————————————————' % port
                    Logging().info(message)
            else:
                message = '---------------端口 %s 未被占用，无需清理----------' % port
                Logging().info(message)

        else:
            assert False, '获取该系统信息出错:system is not in list'

    def _port_is_used(self, port):
        """
        判断端口是否被占用
        :param port: 端口号
        :return: 被占用返回True 未被占用返回False
        """
        system = platform.system()
        if system == 'Darwin':  # MAC 系统
            cmd = subprocess.run(['lsof', '-i:%s' % port], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if len(cmd.stdout) > 0:
                return True
            else:
                return False
        elif system == 'Windows':  # Windows 系统
            p1 = subprocess.Popen(['netstat', '-ano'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            cmd = subprocess.Popen(['findstr', str(port)], stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if len(cmd.stdout.read()) > 0:
                return True
            else:
                return False
        else:
            assert False, '获取该系统信息出错:system is not in list'

    def _create_port_list(self, start_port, number):
        """
        根据设备列表，创建可用的端口列表
        :param start_port: 开始端口
        :param number: 创建个数(int)
        :return: 可用端口列表
        """

        if isinstance(number, int) and number > 0:
            port_list = []
            while len(port_list) != number:
                if not self._port_is_used(start_port):
                    port_list.append(start_port)
                start_port += 1
            return port_list
        else:
            assert '参数number必须为int类型且大于0'

    def _get_android_devices(self):
        """
        获取当前已连接的安卓设备列表
        :return: 返回安卓设备列表
        """
        # 获取安卓设备列表
        p = subprocess.Popen(['adb', 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result_list = [line for line in p.stdout.readlines() if line.strip()]
        if len(result_list) <= 1:
            # 如果获取设备列表为空，则尝试重置adb服务再试(避免因adb服务问题导致的无法获取设备问题)
            subprocess.run('adb kill-server && adb start-server', stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           shell=True)
            p = subprocess.Popen(['adb', 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result_list = [line for line in p.stdout.readlines() if line.strip()]

        device_list = []
        for device in result_list:
            device = device.strip()  # 去除两边的空格、换行符
            if device:
                if isinstance(device, bytes):
                    device_info = bytes.decode(device).split('\t')  # 分割是str字符串的方法，需要把byte类型转换下
                else:
                    device_info = device.split('\t')

                if len(device_info) == 2 and device_info[1] == 'device':
                    device_list.append(device_info[0])
        p.communicate()  # 等待程序执行完毕
        return device_list

#Server().main()
#Server.kill_server('4700')