import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

class FlaskAppTest(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode for CI
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("http://localhost:5000")  # Flask should be running on this port

    def tearDown(self):
        self.driver.quit()

    def test_valid_search_redirects_to_result(self):
        driver = self.driver
        input_field = driver.find_element(By.NAME, "search")
        input_field.clear()
        input_field.send_keys("hello world")
        input_field.send_keys(Keys.RETURN)
        time.sleep(1)  # Wait for redirect

        # Check redirection and display
        self.assertIn("/result", driver.current_url)
        self.assertIn("hello world", driver.page_source)

    def test_xss_input_is_rejected(self):
        driver = self.driver
        input_field = driver.find_element(By.NAME, "search")
        input_field.clear()
        input_field.send_keys("<script>alert('x')</script>")
        input_field.send_keys(Keys.RETURN)
        time.sleep(1)

        # Should stay on home and show error
        self.assertIn("localhost:5000", driver.current_url)
        self.assertIn("Potential XSS attack detected", driver.page_source)

    def test_sql_injection_input_is_rejected(self):
        driver = self.driver
        input_field = driver.find_element(By.NAME, "search")
        input_field.clear()
        input_field.send_keys("' OR '1'='1")
        input_field.send_keys(Keys.RETURN)
        time.sleep(1)

        self.assertIn("localhost:5000", driver.current_url)
        self.assertIn("Potential SQL injection detected", driver.page_source)

if __name__ == "__main__":
    unittest.main()
