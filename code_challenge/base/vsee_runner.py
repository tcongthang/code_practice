from appium import webdriver
from code_challenge.base.helper import Helper
from code_challenge.base.vsee_locators import Locators
from code_challenge.base.appium_server import AppiumServicesHandler
from code_challenge.base.vsee_actions import VSeeMessengerActions

class VSeeMessengerTest(object):

    def __init__(self, desired_caps, user, password, executor='http://localhost:4723/wd/hub'):
        # # set up appium
        self.oHelp = Helper()
        # # self.appium_server = AppiumService()
        # # self.appium_server.start(args=['--session-override', '--address', '127.0.0.1', '-p', '4734', ])
        self.desired_caps = desired_caps
        self.executor = executor
        # get locator definition
        self.locator = Locators(desired_caps['platformName'])
        self.driver = self.__openVsee()
        self.actions = VSeeMessengerActions(self.driver, user, password=password)

    def tearDown(self):
        self.driver.quit()

    def __openVsee(self):

        # Start Appium Server
        # TODO: Thang Truong should have the way to handle appium serve (auto-start, with ip, port ....)
        # todo: Thang Truong - Should we have a better way? example of handle different port & server address
        appium_server = AppiumServicesHandler()
        appium_server.start_server()

        driver = webdriver.Remote(command_executor=self.executor, desired_capabilities=self.desired_caps)
        # Todo:
        driver.implicitly_wait(15)

        self.oHelp.fwrite('INFO: driver.session_id %s' % driver.session_id)
        # make sure the right package and activity were started
        self.oHelp.fwrite('INFO: current_package %s' % driver.current_package)
        self.oHelp.fwrite('INFO: driver.current_activity %s' % driver.current_activity)

        return driver

