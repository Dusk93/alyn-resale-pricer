import logging
import os
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver

import ollama  # For health check

# ... (rest of imports)

def wait_for_ollama():
    for i in range(20):  # Try for ~20 seconds
        try:
            ollama.list()
            print("✅ Ollama server is ready")
            return True
        except:
            print(f"⏳ Waiting for Ollama... ({i+1}/20)")
            time.sleep(2)
    print("⚠️ Ollama not ready after 40 seconds")
    return False

# Dummy server for Render
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_dummy_server():
    port = int(os.getenv("PORT", 8080))
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"✅ Dummy server on port {port}")
        httpd.serve_forever()

def main():
    threading.Thread(target=run_dummy_server, daemon=True).start()
    
    wait_for_ollama()   # Wait for Ollama to start

    # Rest of your bot code (start, handle_photo, etc.)
    # ... (keep the rest as is)
