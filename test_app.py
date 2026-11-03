import json
import subprocess
import time
import unittest
import urllib.request


class ServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.process = subprocess.Popen(
            ["python3", "app.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()
        cls.process.wait()

    def test_health_endpoint(self):
        with urllib.request.urlopen(
            "http://127.0.0.1:8000/health"
        ) as response:
            data = json.loads(response.read())

        self.assertEqual(response.status, 200)
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["service"], "deployment-pipeline-lab")


if __name__ == "__main__":
    unittest.main()