from selenium.webdriver.common.by import By
from code_challenge.base.vsee_locators import Locators
from code_challenge.base.helper import Helper

class VSeeMessengerActions(object):

    def __init__(self, drive, user, password):
        self.locator = Locators()
        self.oHelp = Helper()
        self.user = user
        self.driver = drive
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
        assert self.__wait_element(type=By.XPATH, element=self.locator.xpContacts)

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
                self.switchtoMoreView()

        elif bOnChatBox:
            self.exitChatbox()
            self.switchtoMoreView()

        self.driver.find_element_by_xpath(self.locator.xpSignOut).click()
        return self.__wait_element(type=By.CLASS_NAME, element=self.locator.csWelcome)

    def switchtoContactsView(self):
        self.oHelp.fwrite('Switch to Contacts')
        self.driver.find_element_by_xpath(self.locator.xpContacts).click()
        self.oHelp.sleep(2)

    def switchtoChatsView(self):
        self.oHelp.fwrite('Switch to Chats')
        self.driver.find_element_by_xpath(self.locator.xpChats).click()
        self.oHelp.sleep(2)

    def switchtoCallsView(self):
        self.oHelp.fwrite('Switch to Calls')
        self.driver.find_element_by_xpath(self.locator.xpCalls).click()
        self.oHelp.sleep(2)

    def switchtoMoreView(self):
        self.oHelp.fwrite('Switch to More')
        self.driver.find_element_by_xpath(self.locator.xpMore).click()
        self.oHelp.sleep(2)

    # Function relating to Chats view
    def getlistChatPicker(self):
        """Function to get the list of people we chatted together"""
        org = self.driver.find_element_by_xpath(self.locator.xpChats)
        if org.get_attribute("selected") == 'true':
            self.oHelp.fwrite('ALREADY ON CHATS VIEW')
        else:
            self.switchtoChatsView()
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
        oContact = self.driver.find_element_by_xpath(self.locator.xpContacts)
        if oContact:
            if oContact.get_attribute("selected") == 'true':
                self.oHelp.fwrite('ALREADY ON Contact VIEW')
            else: # Are we on Home-screen but not More tab?
                # Switch to Contacts tab first
                self.switchtoContactsView()

        return self.driver.find_elements(By.XPATH, self.locator.xpLstContact)

    def sendMessage(self, sContact='Test Call', sMessage=None, bTalkedContact=False):
        """
        This is a function to send a message to the Contact who chat together before - showing on Chats view
        :param sContact: People we want to chat
        :param sMessage: text message
        :return: Status of text message or False
        """
        if bTalkedContact:
            self.switchtoChatsView()

        # if contact is NOT in this list of chat history
        else:
            self.startChatFromContactList()

        self.oHelp.sleep(2)
        # Enter message
        self.driver.find_element_by_xpath(self.locator.xpChatEditTextBox).send_keys(sMessage)
        # Click send button
        self.driver.find_element_by_xpath(self.locator.xpSendMessagesBtn).click()
        self.oHelp.sleep(2)
        self.oHelp.fwrite('Message: %s should be sent to %s' % (sMessage, sContact))
        sMessageStatus = self.driver.find_element_by_xpath(self.locator.xpMessageStatus).text

        return sMessageStatus

    def startChatFromChatView(self, sContact='Test Call'):
        """
        This is a function to send a message to the Contact who showing on Chats view
        :param sContact: People we want to chat
        :return: True/False
        """
        # Check if we are on Chat view or not
        oChatView = self.driver.find_elements(By.XPATH, self.locator.xpChats)
        if oChatView:
            if oChatView.get_attribute("selected") == 'true':
                self.oHelp.fwrite('ALREADY ON CHAT VIEW')
            else: # Are we on Home-screen but not More tab?
                self.switchtoChatsView()

        lstPicker = self.getlistChatPicker()
        for oChat in lstPicker:
            if sContact == oChat.text:
                oChat.click()

        return True

    def startChatFromContactList(self, sContact='Test Call'):
        """
        This is a function to send a message to the Contact who has a first chat - not shown on Chats view yet
        :param sContact: People we want to chat
        :return: True/False
        """
        # Check if we are on Chat view or not

        lstContact = self.getlistContact()
        oElement = None
        for sContactElement in lstContact:
            if sContact == sContactElement.text:
                oElement = sContactElement
                break
        if oElement:
            self.oHelp.sleep(2)
            oElement.click()
            self.driver.find_element_by_xpath(self.locator.xpChatIconInContactView).click()
            return True
        else:
            return False

    def exitChatbox(self):
        """
        This is the function to exit the currect chat session
        :return:
        """
        self.oHelp.fwrite('Exiting chat-box')
        self.driver.find_element_by_xpath(self.locator.xpExitChatbox).click()
        self.oHelp.sleep(2)

    def __wait_element(self, type, element, nTimeout=30):
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
        while iTime <= nTimeout:

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
