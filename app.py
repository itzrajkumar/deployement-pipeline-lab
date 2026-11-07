from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os


APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            response = {
                "status": "ok",
                "service": "deployment-pipeline-lab",
            }
            self.send_json(200, response)
        elif self.path == "/version":
            response = {
                "service": "deployment-pipeline-lab",
                "version": APP_VERSION,
            }
            self.send_json(200, response)
        else:
            self.send_response(404)
            self.end_headers()

    def send_json(self, status_code, response):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())


def create_server(host="0.0.0.0", port=8000):
    return HTTPServer((host, port), Handler)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    server = create_server(port=port)
    print(f"Service listening on port {port}", flush=True)
    server.serve_forever()
