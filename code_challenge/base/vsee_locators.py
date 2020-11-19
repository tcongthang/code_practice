
class Locators(object):
    """
    Class to define the locator of element
    """
    def __init__(self, platform='Android'):

        self.platform = platform
        # Maybe this can be handle to check multiple version of app
        base = 'com.vsee.vsee.beta'

        if 'Android' in self.platform:
            self.idUsermail = 'com.vsee.vsee.beta:id/loginEmailEdit'
            self.idPassword = 'com.vsee.vsee.beta:id/loginPasswordEdit'
            self.idSignInBtn = 'com.vsee.vsee.beta:id/loginSignInBut'


            # bottom action bar
            self.idChats = 'Chats'
            self.xpChats = '//androidx.appcompat.app.ActionBar.Tab[@content-desc="Chats"]'

            self.idCalls = 'Calls'
            self.xpCalls = '//androidx.appcompat.app.ActionBar.Tab[@content-desc="Calls"]'

            self.idContacts = 'Contacts'
            self.xpContacts = '//androidx.appcompat.app.ActionBar.Tab[@content-desc="Contacts"]'

            self.idMore = 'More'
            self.xpMore = '//androidx.appcompat.app.ActionBar.Tab[@content-desc="More"]'

            # Element on Contacts screen-view
            self.idSearch = 'contact_list_search_view'
            self.idContactLst = 'com.vsee.vsee.beta:id/contactListView'
            self.csContactView = 'android.view.ViewGroup'
            self.csWelcome = 'android.widget.TextView'
            self.xpLstContact = "//*[@resource-id='com.vsee.vsee.beta:id/itemContactListNameView']"

            # Element on Chats screen-view
            self.xpChatPicker = "//*[@resource-id='com.vsee.vsee.beta:id/chat_picker_name']"
            self.xpTopChatIcon = '//android.widget.TextView[@content-desc="Chat"]'

            # Element on a running Chat view
            self.xpChatText = "//*[@resource-id='com.vsee.vsee.beta:id/chat_picker_background_layout']"
            self.xpSendMessagesBtn = "//*[@resource-id='com.vsee.vsee.beta:id/chatSendBut']"
            self.xpLstMessagesDelivered = "//*[@resource-id='com.vsee.vsee.beta:id/message_text']"
            self.xpChatEditTextBox = "//*[@resource-id='com.vsee.vsee.beta:id/chatEditText']"
            self.xpMessageStatus = "//*[@resource-id='com.vsee.vsee.beta:id/message_status']"
            self.xpExitChatbox = '//android.widget.ImageButton[@content-desc="Navigate up"]'

            self.idLogging = 'com.vsee.vsee.beta:id/loading_text_view'
            self.xpLogging = "//*[@resource-id='com.vsee.vsee.beta:id/loading_text_view']"

            # More view:
            self.xpSignOut = "//*[@resource-id='com.vsee.vsee.beta:id/itemLeftMenuListTextView'][@text='Sign Out']"
            self.xpSettings = "//*[@resource-id='com.vsee.vsee.beta:id/itemLeftMenuListTextView'][@text='Settings']"

        else:
            raise ValueError('ERROR: SHOULD DEFINE EXECUTION PLATFORM HERE Ex: iOS, WinApp ...')

