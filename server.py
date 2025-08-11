#!/usr/bin/env python3
import http.server
import socketserver
import os

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('X-Frame-Options', 'ALLOWALL')
        super().end_headers()

if __name__ == "__main__":
    PORT = 12000
    os.chdir('/workspace/project')
    
    with socketserver.TCPServer(("0.0.0.0", PORT), CORSHTTPRequestHandler) as httpd:
        print(f"Server running at http://0.0.0.0:{PORT}")
        print(f"Access your website at: https://work-1-srsooymslwdgllic.prod-runtime.all-hands.dev")
        httpd.serve_forever()