import unittest
import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class TestSauceDemoLogin(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)

        # Create screenshot folder
        self.screenshot_dir = "screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)

    # 📸 Helper method
    def take_screenshot(self, name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(self.screenshot_dir, f"{name}_{timestamp}.png")
        self.driver.save_screenshot(file_path)
        print(f"📸 Screenshot saved: {file_path}")
        return file_path

    # ✅ POSITIVE TEST
    def test_login_valid_credentials(self):
        driver = self.driver
        driver.get("https://www.saucedemo.com/")

        driver.find_element(By.CSS_SELECTOR, "[data-test='username']").send_keys("standard_user")
        driver.find_element(By.CSS_SELECTOR, "[data-test='password']").send_keys("secret_sauce")
        driver.find_element(By.CSS_SELECTOR, "[data-test='login-button']").click()

        actual_title = driver.find_element(By.CSS_SELECTOR, ".title").text

        try:
            self.assertEqual(actual_title, "Products")
            self.take_screenshot("PASS_valid_login")
        except Exception:
            self.take_screenshot("FAIL_valid_login")
            raise

    # ❌ NEGATIVE TEST - wrong password
    def test_login_invalid_password(self):
        driver = self.driver
        driver.get("https://www.saucedemo.com/")

        driver.find_element(By.CSS_SELECTOR, "[data-test='username']").send_keys("standard_user")
        driver.find_element(By.CSS_SELECTOR, "[data-test='password']").send_keys("wrong_password")
        driver.find_element(By.CSS_SELECTOR, "[data-test='login-button']").click()

        error_message = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text

        try:
            self.assertIn("Username and password do not match", error_message)
            self.take_screenshot("PASS_invalid_password")
        except Exception:
            self.take_screenshot("FAIL_invalid_password")
            raise

    # ❌ NEGATIVE TEST - locked user
    def test_login_locked_out_user(self):
        driver = self.driver
        driver.get("https://www.saucedemo.com/")

        driver.find_element(By.CSS_SELECTOR, "[data-test='username']").send_keys("locked_out_user")
        driver.find_element(By.CSS_SELECTOR, "[data-test='password']").send_keys("secret_sauce")
        driver.find_element(By.CSS_SELECTOR, "[data-test='login-button']").click()

        error_message = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text

        try:
            self.assertIn("locked", error_message.lower())
            self.take_screenshot("PASS_locked_user")
        except Exception:
            self.take_screenshot("FAIL_locked_user")
            raise

    # ❌ NEGATIVE TEST - empty credentials
    def test_login_empty_credentials(self):
        driver = self.driver
        driver.get("https://www.saucedemo.com/")

        driver.find_element(By.CSS_SELECTOR, "[data-test='login-button']").click()

        error_message = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text

        try:
            self.assertTrue(len(error_message) > 0)
            self.take_screenshot("PASS_empty_credentials")
        except Exception:
            self.take_screenshot("FAIL_empty_credentials")
            raise

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
     unittest.main(testRunner=xmlrunner.XMLTestRunner(output='reports'))
