import unittest
from selenium import webdriver
import page


PATH = "/Users/Antonio/AppData/Local/chromedriver.exe"

class SportsEventerTests(unittest.TestCase):

    def setUp(self):
        print("setup")
        self.driver = webdriver.Chrome(PATH)
        self.driver.get("http://127.0.0.1:5000/")

    def test_example(self):
        assert True

    def test_title(self):
        mainPage = page.MainPage(self.driver)
        return mainPage.is_title_matches()

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
