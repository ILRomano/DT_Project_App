import unittest
import requests

class Test(unittest.TestCase):
    def testSiteReachable(self):
        request = requests.get("http://localhost:5000")
        self.assertEqual(200, request.status_code)


if __name__ == '__main__':
    unittest.main()
