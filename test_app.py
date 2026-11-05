import json
import threading
import unittest
import urllib.request

from app import create_server


class ServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Port 0 asks the operating system to choose an available port.
        cls.server = create_server(host="127.0.0.1", port=0)
        cls.port = cls.server.server_address[1]

        cls.server_thread = threading.Thread(
            target=cls.server.serve_forever,
            daemon=True,
        )
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

    def test_health_endpoint(self):
        url = f"http://127.0.0.1:{self.port}/health"

        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())

        self.assertEqual(response.status, 200)
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["service"], "deployment-pipeline-lab")


if __name__ == "__main__":
    unittest.main()