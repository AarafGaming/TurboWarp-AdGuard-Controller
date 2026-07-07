from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import base64
from urllib.parse import unquote

class Bridge(BaseHTTPRequestHandler):
    def do_POST(self):
        self.handle_request('POST')

    def do_GET(self):
        self.handle_request('GET')

    def handle_request(self, method):
        # Path format: /username/password/ENCODED_TARGET_URL
        path = self.path.lstrip('/')
        
        # Split ONLY the first two slashes to get user and pass
        parts = path.split('/', 2)
        
        if len(parts) < 3:
            msg = f"Error: Invalid format. Expected /user/pass/url, got {self.path}"
            print(msg)
            self.send_response(400)
            self.end_headers()
            self.wfile.write(msg.encode())
            return

        username = parts[0]
        password = parts[1]
        encoded_target = parts[2]
        
        # Decode the URL
        target_url = unquote(encoded_target)

        if not target_url.startswith('http'):
            msg = f"Error: Target URL must start with http. Got: {target_url}"
            print(msg)
            self.send_response(400)
            self.end_headers()
            self.wfile.write(msg.encode())
            return

        # Get Body (for POST)
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else None

        # Prepare Auth
        credentials = f"{username}:{password}"
        token = base64.b64encode(credentials.encode()).decode()

        # Forward Request
        req = urllib.request.Request(target_url, data=post_data, method=method)
        req.add_header('Authorization', f'Basic {token}')
        req.add_header('Content-Type', 'application/json')

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(resp.read())
        except Exception as e:
            err_msg = f"--- Forwarding Error: {e} ---"
            print(err_msg)
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    print("Bridge running on http://localhost:9000")
    print("Format: http://127.0.0.1:9000/USER/PASS/ENCODED_URL")
    HTTPServer(('127.0.0.1', 9000), Bridge).serve_forever()   