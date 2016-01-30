import http.server
from agenda.events import load_events
from agenda import report


def run(days, tags, host, port):
    class AgendaHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            try:
                load_events()
            except:
                self.send_response(401)
                self.end_headers()
                raise
            self.send_response(200)
            self.send_header("Content-Type", "text/calendar; charset=utf-8")
            self.end_headers()
            report.ical(days, tags, self.wfile)

    httpd = http.server.HTTPServer((host, port), AgendaHTTPRequestHandler)
    print("Serving on http://{}:{} ...".format(host, port))
    httpd.serve_forever()
