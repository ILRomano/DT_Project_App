import unittest
import time
import app
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class TestApp(unittest.TestCase):

    def testSiteReachable(self):
        request = requests.get("http://10.1.0.68/")
        self.assertEqual(200, request.status_code)

    def testCorrectLocation(self):
        driver = webdriver.Firefox()
        driver.get("http://10.1.0.68/")
        elem = driver.find_element(By.NAME, "city")
        elem.clear()
        elem.send_keys("tel aviv")
        elem.send_keys(Keys.RETURN)
        time.sleep(2)
        self.assertNotIn("Invalid city name", driver.page_source)
        driver.close()

    def testIncorrectLocation(self):
        driver = webdriver.Firefox()
        driver.get("http://10.1.0.68/")
        elem = driver.find_element(By.NAME, "city")
        elem.clear()
        elem.send_keys("tel")
        elem.send_keys(Keys.RETURN)
        time.sleep(2)
        self.assertIn("Invalid city name", driver.page_source)
        driver.close()


if __name__ == '__main__':
    unittest.main()
