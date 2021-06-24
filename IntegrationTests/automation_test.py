import unittest
import yaml
from selenium import webdriver
import page


path_reader = yaml.load(open('path.yaml'))

PATH = path_reader['chromedriver_path']  # /home/uuser/Downloads/chromedriver.exe


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

    def test_user_login(self):
        main_page = page.MainPage(self.driver)
        main_page.click_login()
        login_page = page.LoginPage(self.driver)
        login_page.login_user()
        current_page = page.MainPage(self.driver)
        assert current_page.is_title_matches()
        assert current_page.is_logged_in()

    def test_new_event(self):
        main_page = page.MainPage(self.driver)
        main_page.click_login()
        login_page = page.LoginPage(self.driver)
        login_page.login_user()
        main_page.click_new_event()
        new_event_page = page.NewEventPage(self.driver)
        assert new_event_page.is_title_matches()
        new_event_page.create_event()
        current_page = page.MainPage(self.driver)
        assert current_page.is_title_matches()

    def test_(self):
        pass

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
