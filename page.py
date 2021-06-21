from locator import *
import time


class BasePage:
    def __init__(self, driver):
        self.driver = driver


class MainPage(BasePage):

    def is_title_matches(self):
        return "Home" in self.driver.title

    def click_login(self):
        element = self.driver.find_element(*MainPageLocators.LOGIN_LINK)
        element.click()

    def click_register(self):
        element = self.driver.find_element(*MainPageLocators.REGISTRATION_LINK)
        element.click()


class LoginPage(BasePage):

    def is_title_matches(self):
        return "Login" in self.driver.title


class RegisterPage(BasePage):

    def is_title_matches(self):
        return "Register" in self.driver.title

    def input_invalid_email(self):
        email = self.driver.find_element(*RegisterPageLocators.EMAIL_INPUT)
        email.send_keys("invalid")
        element = self.driver.find_element(*RegisterPageLocators.SUBMIT_BUTTON)
        element.click()
        time.sleep(1)
        try:
            self.driver.find_element(*RegisterPageLocators.ERROR_MESSAGE)
        except:
            return False
        return True
