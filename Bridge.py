from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import base64

class Bridge(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Get data from TurboWarp
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # 2. Forward to AdGuard
        url = 'http://192.168.1.20:8083/control/dns_config'
        credentials = 'admin:AarafGamingYT' # UPDATE THIS
        token = base64.b64encode(credentials.encode()).decode()
        
        req = urllib.request.Request(url, data=post_data, method='POST')
        req.add_header('Authorization', f'Basic {token}')
        req.add_header('Content-Type', 'application/json')
        
        try:
            with urllib.request.urlopen(req) as resp:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(resp.read())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
    def do_GET(self):
        # Forward GET requests to AdGuard status endpoint
        if self.path == '/stats':
                url = 'http://192.168.1.20:8083/control/stats'
        else:
	        url = 'http://192.168.1.20:8083/control/status'
        credentials = 'admin:AarafGamingYT'
        token = base64.b64encode(credentials.encode()).decode()
        
        req = urllib.request.Request(url, method='GET')
        req.add_header('Authorization', f'Basic {token}')
        
        try:
            with urllib.request.urlopen(req) as resp:
                data = resp.read()
                # Send response back to TurboWarp
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(data)
        except Exception as e:
            print(f"--- GET ERROR: {e} ---")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())   

print("Bridge running on http://localhost:9000")
HTTPServer(('127.0.0.1', 9000), Bridge).serve_forever()   