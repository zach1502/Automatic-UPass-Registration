import sys
import time
import os
import pickle as pkl # save last used browser (if manually inputted)
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.support.ui import Select


class UPass:
    # Did I need to make it a class? No. but maybe it'll be useful for portability
    data = {
    'school': 'sfu',
    'school-login-username': 'zach1502',
    'school-login-password': 'aStrongPasswordIHope?',
    'compass-card-number': "123123123123123123",
    'compass-card-cvn': "123",
    }

    def __init__(self) -> None:
        self.init_browser()

    def find_browser(self):
        # check if C:\Program Files\Google\Chrome\Application\chrome.exe exists
        # if it does, return that path
        default_chrome_path = os.path.join("C:", os.sep, "Program Files", "Google", "Chrome", "Application", "chrome.exe")
        default_brave_path = os.path.join("C:", os.sep, "Program Files (x86)", "BraveSoftware", "Brave-browser", "Application", "brave.exe")
        # default_edge_path = os.path.join("C:", os.sep, "Program Files (x86)", "Microsoft", "Edge", "Application", "msedge.exe")

        if os.path.isfile(default_chrome_path):
            return default_chrome_path
        elif os.path.isfile(default_brave_path):
            return default_brave_path
        # elif os.path.isfile(default_edge_path):
        #     return default_edge_path
        else:
            # ask user to manually enter path
            return None

    def init_browser(self):
        driver_path = "chromedriver.exe"
        browser_path = self.find_browser()
        while(not os.path.isfile(browser_path)):
            print("Finding browser automatically failed.")
            print("Follow the instructions on the GitHub page to manually enter the path to your browser.")
            browser_path = input("Please enter the path to your Chrome executable (chrome.exe, etc.):\n ")

        option = webdriver.ChromeOptions()
        option.add_argument('log-level=3')
        #option.add_argument("--headless") # iframes hate this

        option.binary_location = browser_path
        self.browser = webdriver.Chrome(executable_path=driver_path, options=option)

    def get_data_from_user(self):
        # Ask for inputs
        print("Feel free to check the code to see what it does if you're at all concerned. It's open source and you're welcome to contribute.")
        print("Please fill out the following information:")
        self.data['school'] = input("Enter your school (sfu, ubc, etc.): ").lower()
        self.data['school-login-username'] = input("Enter your school login username: ")
        self.data['school-login-password'] = input("Enter your school login password: ")
        print("If your compass card is already linked, there should be no need to fill the following out.")
        self.data['compass-card-number'] = input("Enter your compass card number: ")
        self.data['compass-card-cvn'] = input("Enter your compass card cvn: ")

    def go_to_upass_page(self):
        # Go to upass page
        print("Going to U-Pass page...")
        self.browser.get("https://upassbc.translink.ca/")

    def select_school(self):
        print("Selecting School...")
        select = Select(self.browser.find_element(by="id", value="PsiId"))
        select.select_by_value(self.data['school'])
        self.browser.find_element(by="id", value="goButton").click()

    def login_to_school(self):
        print("Logging in to School Website...")
        self.browser.find_element(by="id", value="username").send_keys(self.data['school-login-username'])
        self.browser.find_element(by="id", value="password").send_keys(self.data['school-login-password'])

        # find an element with the name Sign In
        if(self.data['school'] == 'sfu'):
            self.browser.find_element(by="name", value="submit").click()
        elif(self.data['school'] == 'ubc'):
            self.browser.find_element(by="name", value="_eventId_proceed").click()
        else:
            print("Sorry, your school is not supported yet. If you think this is an error, please open an issue on GitHub.")
            self.browser.quit()
            sys.exit()

        if("Failed" in self.browser.page_source):
            print("Login failed. Please check your credentials and try again.")
            self.browser.quit()
            sys.exit()

    def check_for_mfa(self):
        return "Authentication" in self.browser.page_source

    def handle_mfa(self):
        print()
        print()
        print("#####################################")
        print("Additional Authentication Required!!!")
        print("#####################################")
        print()
        print()
        if(self.data['school'] == 'sfu'):
            print("MAKE SURE YOU ENTER THE MFA CODE CORRECTLY!")
            mfaCode = input("Enter MFA code: ")
            self.browser.switch_to.frame(self.browser.find_element_by_tag_name("iframe"))
            self.browser.find_element(by="id", value="totpCode").send_keys(mfaCode)
            #self.browser.find_element_by_tag_name("button").click() ???? Doesn't work????
            self.browser.find_elements_by_css_selector(".submit")[0].click()
            self.browser.switch_to.default_content()
        elif(self.data['school'] == 'ubc'):
            self.browser.switch_to.frame(self.browser.find_element_by_tag_name("iframe"))
            # probably will call first
            self.browser.find_elements_by_css_selector("button.positive")[0].click()
            self.browser.switch_to.default_content()
        else:
            print("Sorry, your school is not supported yet. Please open an issue on GitHub.")
            self.browser.quit()
            sys.exit()

    def check_if_compass_card_unlinked(self):
        return "Link a Compass Card" in self.browser.page_source

    def handle_unlinked_compass_card(self):
        print("Linking Compass Card...")
        WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located((By.ID, "link-CompassNumber"))
        ).send_keys(self.data['compass-card-number'])
        self.browser.find_element(by="id", value="link-CVN").send_keys(self.data['compass-card-cvn'])
        self.browser.find_element(by="id", value="btnLink").click()

    def apply_for_upass(self):
        time.sleep(1)
        print("Applying for U-Pass...")
        # find and select radio button
        try:
            self.browser.find_element(by="id", value="chk_1").click()
        except ElementNotVisibleException:
            raise ElementNotVisibleException("Could not find the checkbox. Perhaps you already applied for a U-Pass?")
        except Exception as e:
            # something unexpected happened
            raise e

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, "requestButton"))
        ).click()

    def success(self):
        print("SUCCESS!!!")
        print("Browser will automatically close now!")
        time.sleep(2)
        self.browser.quit()
    
    def failed(self, msg = None):
        print(msg if msg else "Failed to apply for U-Pass. Please try again.")
        self.browser.quit()
        sys.exit()


if __name__ == "__main__":
    print("DO NOT CLOSE THE NEWLY OPENED BROWSER WINDOW. IT WILL CLOSE AUTOMATICALLY WHEN DONE. CLOSING THE BROWSER WILL CAUSE THE SCRIPT TO FAIL.")
    print("DO NOT CLOSE THE NEWLY OPENED BROWSER WINDOW. IT WILL CLOSE AUTOMATICALLY WHEN DONE. CLOSING THE BROWSER WILL CAUSE THE SCRIPT TO FAIL.")
    print("DO NOT CLOSE THE NEWLY OPENED BROWSER WINDOW. IT WILL CLOSE AUTOMATICALLY WHEN DONE. CLOSING THE BROWSER WILL CAUSE THE SCRIPT TO FAIL.")
    print("DO NOT CLOSE THE NEWLY OPENED BROWSER WINDOW. IT WILL CLOSE AUTOMATICALLY WHEN DONE. CLOSING THE BROWSER WILL CAUSE THE SCRIPT TO FAIL.")
    print("DO NOT CLOSE THE NEWLY OPENED BROWSER WINDOW. IT WILL CLOSE AUTOMATICALLY WHEN DONE. CLOSING THE BROWSER WILL CAUSE THE SCRIPT TO FAIL.")
    print("DO NOT CLOSE THE NEWLY OPENED BROWSER WINDOW. IT WILL CLOSE AUTOMATICALLY WHEN DONE. CLOSING THE BROWSER WILL CAUSE THE SCRIPT TO FAIL.")

    bot = UPass()
    bot.get_data_from_user()
    bot.go_to_upass_page()
    bot.select_school()
    bot.login_to_school()

    if(bot.check_for_mfa()):
        bot.handle_mfa()

    if(bot.check_if_compass_card_unlinked()):
        bot.handle_unlinked_compass_card()

    bot.apply_for_upass()
    bot.success()
