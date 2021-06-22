import unittest
from selenium import webdriver
import page

PATH = "/home/uuser/Downloads/chromedriver.exe"


class SportsEventerTests(unittest.TestCase):

    def setUp(self):
        print("setup")
        self.driver = webdriver.Chrome(PATH)
        self.driver.get("http://127.0.0.1:5000/")

    def test_title(self):
        main_page = page.MainPage(self.driver)
        assert main_page.is_title_matches()

    def test_login_relocating(self):
        main_page = page.MainPage(self.driver)
        main_page.click_login()
        login_page = page.LoginPage(self.driver)
        assert login_page.is_title_matches()

    def test_register_relocating(self):
        main_page = page.MainPage(self.driver)
        main_page.click_register()
        register_page = page.RegisterPage(self.driver)
        assert register_page.is_title_matches()

    def test_email_verification(self):
        main_page = page.MainPage(self.driver)
        main_page.click_register()
        register_page = page.RegisterPage(self.driver)
        assert register_page.input_invalid_email()

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
