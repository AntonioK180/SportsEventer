from locator import *


class BasePage():
    def __init__(self, driver):
        self.driver = driver


class MainPage(BasePage):

    def is_title_matches(self):
        return "Home" in self.driver.title

    def click_login(self):
        element = self.driver.find_element(*MainPageLocators.LOGIN_LINK)
        element.click()


class LoginPage(BasePage):
    pass
