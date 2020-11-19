from selenium.webdriver.common.by import By
from code_challenge.base.vsee_locators import Locators
from code_challenge.base.helper import Helper

class VSeeMessengerActions(object):

    def __init__(self, drive, user, password):
        self.oHelp = Helper()
        self.driver = drive
        self.locator = Locators()
        self.user = user
        self.password = password

    def tearDown(self):
        """Function to sign out & close"""
        self.signout()
        self.oHelp.fwrite("Bye & See you soon VSee Messenger")
        self.driver.quit()

    def login(self):
        self.oHelp.fwrite('Enter username/email - %s' % self.user)
        self.driver.find_element_by_id(self.locator.idUsermail).send_keys(self.user)

        self.oHelp.fwrite('Enter credential - %s' % self.password)
        self.driver.find_element_by_id(self.locator.idPassword).send_keys(self.password)

        self.oHelp.fwrite('Press SignIn button')
        self.driver.find_element_by_id(self.locator.idSignInBtn).click()

    def signout(self, bOnChatBox=True):
        """
        Function to signout on Vsee Messenger app base on the current UI
        :param bOnChatBox: if we are on chat box view
        TODO: Need to define more/Improvement .....Auto detect where we are. etc
        :return:
        """

        # Check if
        oMore = self.driver.find_elements(By.XPATH, self.locator.xpMore)
        if oMore:
            if oMore.get_attribute("selected") == 'true':
                self.oHelp.fwrite('ALREADY ON MORE VIEW')
            else: # Are we on Home-screen but not More tab?
                self.switchtoMore()

        elif bOnChatBox:
            self.exitChatbox()
            self.switchtoMore()

        self.driver.find_element_by_xpath(self.locator.xpSignOut).click()
        return self.__waitforelement(type=By.CLASS_NAME, element=self.locator.csWelcome)

    def switchtoContacts(self):
        self.oHelp.fwrite('Switch to Contacts')
        self.driver.find_element_by_xpath(self.locator.xpContacts).click()
        self.oHelp.sleep(2)

    def switchtoChats(self):
        self.oHelp.fwrite('Switch to Chats')
        self.driver.find_element_by_xpath(self.locator.xpChats).click()
        self.oHelp.sleep(2)

    def switchtoCalls(self):
        self.oHelp.fwrite('Switch to Calls')
        self.driver.find_element_by_xpath(self.locator.xpCalls).click()
        self.oHelp.sleep(2)

    def switchtoMore(self):
        self.oHelp.fwrite('Switch to More')
        self.driver.find_element_by_xpath(self.locator.xpMore).click()
        self.oHelp.sleep(2)

    # Function relating to Chats view
    def getlistChatPicker(self):
        org = self.driver.find_element_by_xpath(self.locator.xpChats)
        if org.get_attribute("selected") == 'true':
            self.oHelp.fwrite('ALREADY ON CHATS VIEW')
        else:
            self.switchtoChats()
        return self.driver.find_elements(By.XPATH, self.locator.xpChatPicker)

    # Function relating to Contacts view
    def findContact(self, sContact):
        """
        Find if the contact is on the list or not
        :param sContact: Name of contact
        :return:
        """
        for element in self.getlistContact():
            if sContact == element.text:
                return element

        return False

    def getlistContact(self):
        """
        Function to get the list of current Contacts
        :return:
        """
        # Switch to Contacts tab first
        self.switchtoContacts()
        return self.driver.find_elements(By.XPATH, self.locator.xpLstContact)

    def sendMessage(self, sContact='Test Call', sMessage=None):
        """
        This is a function to send a message to the Contact who chat together before - showing on Chats view
        :param sContact: People we want to chat
        :param sMessage: text message
        :return: Status of text message or False
        """
        lstPicker = self.getlistChatPicker()
        self.oHelp.sleep(2)
        for oChat in lstPicker:
            if sContact == oChat.text:
                oChat.click()
                # self.sleep(2)
                self.driver.find_element_by_xpath(self.locator.xpChatEditTextBox).send_keys(sMessage)
                # self.sleep(2)
                # Click send button
                self.driver.find_element_by_xpath(self.locator.xpSendMessagesBtn).click()
                self.oHelp.sleep(2)
                self.driver.get_screenshot_as_png()
                self.oHelp.fwrite('Message: %s should be sent to %s' % (sMessage, sContact))
                sMessageStatus = self.driver.find_element_by_xpath(self.locator.xpMessageStatus).text

                return sMessageStatus

        self.oHelp.fwrite('Hey, Look likes the you have never sent message to %s - should use another way' % sContact)

        return False

    def sendFirstMessage(self, sContact='Test Call', sMessage=None):
        """
        This is a function to send a message to the Contact who has a first chat - not shown on Chats view yet
        :param sContact: People we want to chat
        :param sMessage: text message
        :return: Status of text message
        """
        # Switch to Contacts tab first
        self.switchtoContacts()
        lstContact = self.getlistContact()
        oElement = None
        for sContactElement in lstContact:
            if sContact == sContactElement.text:
                oElement = sContactElement
        self.oHelp.sleep(5)
        oElement.click()

    def exitChatbox(self):
        """
        This is the function to exit the currect chat session
        :return:
        """
        self.oHelp.fwrite('EXIT CHAT BOX')
        self.driver.find_element_by_xpath(self.locator.xpExitChatbox).click()
        self.oHelp.sleep(2)

    def __waitforelement(self, type, element, nTimeout=30):
        """
        Function to wait for a element to be shown up
        :param type: type of element: By.CLASS_NAME, By.ID, By.XPATH or so on
        :param element: value of element
        :param nTimeout: maximum time to wait for element
        :return: True if see the element else False
        """
        bIsPresent = False
        nInterval = 5
        iTime = 0
        while nInterval <= nTimeout:

            findelement = self.driver.find_elements(type, element)

            if len(findelement) > 0:
                bIsPresent = True
                self.oHelp.fwrite('element %s is found after %s' % (element, iTime))
                break
            else:
                self.oHelp.sleep(nInterval)
                self.oHelp.fwrite('Waiting for element showing %s' % iTime)

            iTime += nInterval

        if not bIsPresent:
            self.oHelp.fwrite('Do not see %s after %s' % (element, nTimeout))

        return bIsPresent


    ######### On-going function ###################

    def test_home_screen(self):
        self.oHelp.fwrite('Check to make sure new contact/group icon is shown')
        self.driver.find_element_by_id('com.vsee.vsee.beta:id/action_add')

        self.oHelp.fwrite('Check to make sure Chats tab icon is shown')

        self.driver.find_element_by_accessibility_id(self.locator.idChats)
        self.driver.find_element_by_xpath(self.locator.xpChats)
        self.oHelp.fwrite('Check to make sure the Calls tab icon is shown')

        self.driver.find_element_by_accessibility_id(self.locator.idCalls)
        self.driver.find_element_by_xpath(self.locator.xpCalls)
        self.oHelp.fwrite('Check to make sure the Contacts tab icon is shown')

        self.driver.find_element_by_accessibility_id(self.locator.idContacts)
        self.driver.find_element_by_xpath(self.locator.xpContacts)
        self.oHelp.fwrite('Check to make sure the More icon is shown')

        self.driver.find_element_by_accessibility_id(self.locator.idMore)
        self.driver.find_element_by_xpath(self.locator.xpMore)

        self.oHelp.fwrite('Check to make sure the Search Contacts box is shown')
        self.driver.find_element_by_id(self.locator.idSearch)


    def startNewChat(self):
        """
        Function to start a
        :return:
        """
        self.driver.find_element_by_xpath(self.locator.xpTopChatIcon).click()