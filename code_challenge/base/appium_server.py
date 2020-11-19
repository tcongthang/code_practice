import subprocess
import os
from multiprocessing import Process
import threading
from .helper import Helper

class AppiumServicesHandler(object):

    def __init__(self, port=4723, idevice=0):
        self.oHelper = Helper()
        self.port = port
        self.adv = self.__avd_devices()
        self.devices = self.__attached_devices()[idevice]

    def start_server(self):
        """start the appium server
        """
        cmd = "appium --session-override --log-level error:error -p %s -U %s" % (self.port, self.devices)
        # os.system(cmd)
        # time.sleep(10)
        t1 = RunServer(cmd)
        p = Process(target=t1.start())
        p.start()
        self.oHelper.sleep(10)
        self.oHelper.fwrite('Appium services started - %s' % cmd)

    def __attached_devices(self):
        devices = []
        result = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE).stdout.readlines()

        # Should be improved in case of multiple device
        for item in result:
            t = item.decode().split("\tdevice")
            if len(t) >= 2:
                devices.append(t[0])
        self.oHelper.fwrite('List of ADB devices %s ' % devices)
        return devices

    def __avd_devices(self):

        avd = []
        result = subprocess.Popen("emulator -list-avds", shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE).stdout.readlines()

        for item in result:
            t = item.decode().split("\r")
            if len(t) >= 2:
                avd.append(t[0])

        self.oHelper.fwrite('List of AVD devices %s ' % avd)
        return avd


class RunServer(threading.Thread):
    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd

    def run(self):
        os.system(self.cmd)
