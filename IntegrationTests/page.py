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

    def click_new_event(self):
        element = self.driver.find_element(*MainPageLocators.NEW_EVENT_LINK)
        element.click()

    def is_logged_in(self):
        try:
            self.driver.find_element(*MainPageLocators.NEW_EVENT_LINK)
            self.driver.find_element(*MainPageLocators.MY_PROFILE_LINK)
        except:
            return False
        return True


class LoginPage(BasePage):

    def is_title_matches(self):
        return "Login" in self.driver.title

    def login_user(self):
        username_input = self.driver.find_element(*LoginpageLocators.NAME_INPUT)
        username_input.send_keys("as")
        password_input = self.driver.find_element(*LoginpageLocators.PASSWORD_INPUT)
        password_input.send_keys("as")
        time.sleep(1)
        submit_button = self.driver.find_element(*LoginpageLocators.SUBMIT_BUTTON)
        submit_button.click()


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


class NewEventPage(BasePage):

    def is_title_matches(self):
        return "Create an Event" in self.driver.title

    def create_event(self):
        participating_input = self.driver.find_element(*NewEventPageLocators.PARTICIPATING_INPUT)
        participating_input.send_keys(2)
        needed_input = self.driver.find_element(*NewEventPageLocators.NEEDED_INPUT)
        needed_input.send_keys(5)
        date_input = self.driver.find_element(*NewEventPageLocators.DATE_INPUT)
        date_input.clear()
        date_input.send_keys("09-20-2021")
        time_input = self.driver.find_element(*NewEventPageLocators.TIME_INPUT)
        time_input.clear()
        time_input.send_keys("0340AM")
        price_input = self.driver.find_element(*NewEventPageLocators.PRICE_INPUT)
        price_input.send_keys(6)
        time.sleep(1)

        submit_btn = self.driver.find_element(By.ID, "submit_btn")
        submit_btn.click()
