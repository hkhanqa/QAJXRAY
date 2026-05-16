import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestSauceDemoLogin(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_AT_2_login(self):
        driver = self.driver

        driver.get("https://www.saucedemo.com/")

        # Enter username
        driver.find_element(By.CSS_SELECTOR, "*[data-test='username']").send_keys("standard_user")

        # Enter password
        driver.find_element(By.CSS_SELECTOR, "*[data-test='password']").send_keys("secret_sauce")

        # Click login button
        driver.find_element(By.CSS_SELECTOR, "*[data-test='login-button']").click()

        # Validate login success
        actual_title = driver.find_element(By.CSS_SELECTOR, ".title").text
        self.assertEqual(actual_title, "Products")

        print("Test passed")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()