import unittest
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from pyvirtualdisplay import Display
import chromedriver_autoinstaller

class LocationSearch(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up a virtual display for all tests"""
        cls.display = Display(visible=0, size=(800, 600))
        cls.display.start()

    @classmethod
    def tearDownClass(cls):
        """Stop the virtual display after all tests"""
        cls.display.stop()

    def setUp(self):
        """Set up the Chrome driver with options for headless execution"""
        chromedriver_autoinstaller.install()  # Automatically install chromedriver

        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Get the Docker IP from the environment variable
        ip_address = os.getenv("HOST_IP")
        self.url = f"http://{ip_address}:5000" 

    def test_positive_location(self):
        self.set_location("haifa")
        self.assertEqual((self.driver.find_element(By.CLASS_NAME, "text-capitalize")).text, "Haifa Israel")
        
    def test_negative_location(self):
        """
        This method calls the set_location with the input,
        and asserts that the website: 
        -displays the correct location information 
        -does not display the entered invalid location.
        """
        self.set_location("fakelocation")
        self.assertNotEqual((self.driver.find_element(By.CLASS_NAME, "fw-normal")).text, "fakelocation")        

    def set_location(self, location):
        """
        This method simulates entering an invalid/valid location into the search input field,
        submitting the form and returning the driver
        """
        self.driver.get(self.url)
        userEl = self.driver.find_element(By.NAME, "username")
        passEl = self.driver.find_element(By.NAME, "password")
        userEl.send_keys("test")
        passEl.send_keys("123")
        loginEl = self.driver.find_element(By.CLASS_NAME, "btn-primary")
        loginEl.click()
        locationEl = self.driver.find_element(By.NAME, "location")
        locationEl.send_keys(location)
        submitEl = self.driver.find_element(By.ID, "search-addon")
        submitEl.click()
        time.sleep(2)

    def tearDown(self):
        """Close the browser after each test"""
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

