from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

my_id = '1149817'


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        result = my_id + ', ' + str(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        self.wfile.write(bytes(result, "utf-8"))


if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)

    try:
        print('Server is running...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        print('Server stopped')
