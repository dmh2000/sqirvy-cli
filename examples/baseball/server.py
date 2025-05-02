import http.server
import socketserver
import json
import os

PORT = 8080
SCHEDULE_FILE = "schedule.json"
INDEX_FILE = "index.html"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = INDEX_FILE
            # Let SimpleHTTPRequestHandler handle serving index.html
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == '/schedule/json':
            try:
                # Check if schedule file exists
                if not os.path.exists(SCHEDULE_FILE):
                    self.send_error(404, f"File Not Found: {SCHEDULE_FILE}")
                    return

                # Read and serve the JSON file content
                with open(SCHEDULE_FILE, 'rb') as file:
                    content = file.read()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*') # Add CORS header
                self.end_headers()
                self.wfile.write(content)

            except FileNotFoundError:
                 self.send_error(404, f"File Not Found: {SCHEDULE_FILE}")
            except Exception as e:
                self.send_error(500, f"Internal Server Error: {e}")
        else:
            # Let SimpleHTTPRequestHandler handle other file requests
            # Ensure CORS for any potential static assets requested by index.html
            self.send_header('Access-Control-Allow-Origin', '*')
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

    # Add OPTIONS handler for CORS preflight requests if needed by complex JS
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        self.end_headers()


# Ensure schedule.json exists (create a dummy if not)
if not os.path.exists(SCHEDULE_FILE):
    print(f"Warning: {SCHEDULE_FILE} not found. Creating a dummy file.")
    dummy_data = [
      {
        "away_team_full": "Sample Team A",
        "away_team_abbr": "STA",
        "home_team_full": "Sample Team B",
        "home_team_abbr": "STB",
        "time": "1:00 PM"
      }
    ]
    try:
        with open(SCHEDULE_FILE, 'w') as f:
            json.dump(dummy_data, f, indent=2)
    except IOError as e:
        print(f"Error creating dummy {SCHEDULE_FILE}: {e}")
        # Optionally exit if the file cannot be created
        # exit(1)

Handler = CustomHandler

# Use ThreadingTCPServer for potentially better handling of multiple requests
# For strictly basic use as requested, TCPServer is fine.
# httpd = socketserver.TCPServer(("", PORT), Handler)
httpd = socketserver.ThreadingTCPServer(("", PORT), Handler)

print(f"Serving HTTP on port {PORT}...")
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped.")
    httpd.shutdown()
    httpd.server_close()

