from appium.webdriver.appium_service import AppiumService

appium_server = AppiumService()
appium_server.start()
appium_server.stop()