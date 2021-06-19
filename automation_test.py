from selenium import webdriver
import time


PATH = "/usr/local/share/chromedriver"
driver = webdriver.Chrome(PATH)

driver.get("http://127.0.0.1:5000/")

search = driver.find_element_by_id("registration_link")
time.sleep(2)
search.click()

time.sleep(5)

driver.quit()
