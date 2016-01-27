import http.server
from agenda import report


def run(days, host, port):
    class AgendaHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/calendar; charset=utf-8")
            self.end_headers()
            report.ical(days, self.wfile)

    httpd = http.server.HTTPServer((host, port), AgendaHTTPRequestHandler)
    print("Serving on http://{}:{} ...".format(host, port))
    httpd.serve_forever()
