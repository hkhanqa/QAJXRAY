import unittest
import os
import sys
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import xmlrunner

# ✅ FIX: force UTF-8 (prevents encoding issues in Jenkins)
sys.stdout.reconfigure(encoding='utf-8')


class TestSauceDemoLogin(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)

        # Create folders safely
        os.makedirs("reports", exist_ok=True)
        os.makedirs("screenshots", exist_ok=True)

    # =========================
    # 📸 Screenshot helper
    # =========================
    def take_screenshot(self, name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"screenshots/{name}_{timestamp}.png"

        self.driver.save_screenshot(path)

        # ✅ NO EMOJI (fix Jenkins crash)
        print(f"Screenshot saved: {path}")

        return path

    # =========================
    # ✅ POSITIVE TEST
    # =========================
    def test_XA_1_login_valid_credentials(self):
        driver = self.driver
        driver.get("https://www.saucedemo.com/")

        driver.find_element(By.CSS_SELECTOR, "[data-test='username']").send_keys("standard_user")
        driver.find_element(By.CSS_SELECTOR, "[data-test='password']").send_keys("secret_sauce")
        driver.find_element(By.CSS_SELECTOR, "[data-test='login-button']").click()

        try:
            title = driver.find_element(By.CSS_SELECTOR, ".title").text
            self.assertEqual(title, "Products")
            self.take_screenshot("test_login_valid_credentials_PASS")
        except Exception:
            self.take_screenshot("test_login_valid_credentials_FAIL")
            raise

    # =========================
    # ❌ NEGATIVE TEST - wrong password
    # =========================
    def test_XA_1_login_invalid_password(self):
        driver = self.driver
        driver.get("https://www.saucedemo.com/")

        driver.find_element(By.CSS_SELECTOR, "[data-test='username']").send_keys("standard_user")
        driver.find_element(By.CSS_SELECTOR, "[data-test='password']").send_keys("wrong_pass")
        driver.find_element(By.CSS_SELECTOR, "[data-test='login-button']").click()

        error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text

        try:
            self.assertIn("Username and password do not match", error)
            self.take_screenshot("test_login_invalid_password_PASS")
        except Exception:
            self.take_screenshot("test_login_invalid_password_FAIL")
            raise

    # =========================
    # ❌ NEGATIVE TEST - locked user
    # =========================
    def test_XA_1_login_locked_user(self):
        driver = self.driver
        driver.get("https://www.saucedemo.com/")

        driver.find_element(By.CSS_SELECTOR, "[data-test='username']").send_keys("locked_out_user")
        driver.find_element(By.CSS_SELECTOR, "[data-test='password']").send_keys("secret_sauce")
        driver.find_element(By.CSS_SELECTOR, "[data-test='login-button']").click()

        error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text

        try:
            self.assertIn("locked", error.lower())
            self.take_screenshot("test_login_locked_user_PASS")
        except Exception:
            self.take_screenshot("test_login_locked_user_FAIL")
            raise

    # =========================
    # ❌ NEGATIVE TEST - empty login
    # =========================
    def test_XA_1_login_empty_credentials(self):
        driver = self.driver
        driver.get("https://www.saucedemo.com/")

        driver.find_element(By.CSS_SELECTOR, "[data-test='login-button']").click()

        error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text

        try:
            self.assertTrue(len(error) > 0)
            self.take_screenshot("test_login_empty_credentials_PASS")
        except Exception:
            self.take_screenshot("test_login_empty_credentials_FAIL")
            raise

    def tearDown(self):
        self.driver.quit()


# =========================
# 🚀 RUNNER (JENKINS READY)
# =========================
if __name__ == "__main__":
    unittest.main(
          testRunner=xmlrunner.XMLTestRunner(output='reports'),
        verbosity=2
    )
