import unittest
import warnings
from api import app


class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Welcome to the Pilipens!</p>")

    def test_getcountry(self):
        response = self.app.get("/country")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Afghanistan" in response.data.decode())

    def test_getcountry_by_id(self):
        response = self.app.get("/country/68")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("New Zealand" in response.data.decode())

    def test_addcountry(self):
        data = {
            "country": "Zimbabwe"
        }
        response = self.app.post("/country", json=data)
        self.assertEqual(response.status_code, 201)

    def test_updatecountry(self):
        data = {
            "country": "Pilepines"
        }
        response = self.app.put("/country/110", json=data)
        self.assertEqual(response.status_code, 201)

    def test_deletecountry(self):
        response = self.app.delete("/country/110")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()