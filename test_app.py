import json
import subprocess
import time
import unittest
import urllib.request
from urllib.error import URLError


class ServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.process = subprocess.Popen(
            ["python3", "app.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        health_url = "http://127.0.0.1:8000/health"
        deadline = time.monotonic() + 5

        while time.monotonic() < deadline:
            if cls.process.poll() is not None:
                raise RuntimeError("The service stopped before it became ready.")

            try:
                with urllib.request.urlopen(health_url, timeout=1):
                    return
            except URLError:
                time.sleep(0.1)

        cls.process.terminate()
        cls.process.wait()
        raise RuntimeError("The service did not become ready within 5 seconds.")

    @classmethod
    def tearDownClass(cls):
        if cls.process.poll() is None:
            cls.process.terminate()
            cls.process.wait()

    def test_health_endpoint(self):
        url = "http://127.0.0.1:8000/health"

        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())

        self.assertEqual(response.status, 200)
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["service"], "deployment-pipeline-lab")


if __name__ == "__main__":
    unittest.main()