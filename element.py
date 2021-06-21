from selenium.webdriver.support.ui import WebDriverWait

class BasePageElement():
    def __init__(self, locator):
        self.locator = locator

    def __set__(self, instance, value):
        driver = instance.driver()
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element_by_name(self.locator))
        driver.find_element_by_name(self.locator).clear()
        driver.find_element_by_name(self.locator).send_keys(value)

    def __get__(self, instance, owner):
        driver = instance.driver()
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element_by_name(self.locator))
        element = driver.find_element_by_name(self.locator)
        return element.get_attribute("value")