from locator import *
from element import BasePageElement


class BasePage():
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
    input_email_element = BasePageElement("email")

    def is_title_matches(self):
        return "Register" in self.driver.title

    def input_email(self):
        input_email_element = "valid@gmail.com"
        element = self.driver.find_element(*RegisterPageLocators.SUBMIT_BUTTON)
        element.click()
        self.driver.find_element(*RegisterPageLocators.ERROR_MESSAGE)
        return False
