from selenium.webdriver.common.by import By


class MainPageLocators:
    LOGIN_LINK = (By.ID, "login_link")
    REGISTRATION_LINK = (By.ID, "registration_link")


class LoginpageLocators:
    pass


class RegisterPageLocators:
    EMAIL_INPUT = (By.ID, "email")
    SUBMIT_BUTTON = (By.ID, "sign_button")
    ERROR_MESSAGE = (By.ID, "error")