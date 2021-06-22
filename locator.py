from selenium.webdriver.common.by import By


class MainPageLocators:
    LOGIN_LINK = (By.ID, "login_link")
    REGISTRATION_LINK = (By.ID, "registration_link")
    NEW_EVENT_LINK = (By.ID, "newEvent")
    MY_PROFILE_LINK = (By.ID, "myProfile")


class LoginpageLocators:
    NAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "pwd")
    SUBMIT_BUTTON = (By.ID, "login_button")


class RegisterPageLocators:
    EMAIL_INPUT = (By.ID, "email")
    SUBMIT_BUTTON = (By.ID, "sign_button")
    ERROR_MESSAGE = (By.ID, "error")


class NewEventPageLocators:
    PARTICIPATING_INPUT = (By.ID, "participating")
    NEEDED_INPUT = (By.ID, "needed")
    DATE_INPUT = (By.ID, "date")
    TIME_INPUT = (By.ID, "time")
    PRICE_INPUT = (By.ID, "price")
    SUBMIT_BUTTON = (By.ID, "submit_btn")
