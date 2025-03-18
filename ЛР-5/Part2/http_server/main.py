import http.server
import json
import os
import sqlite3
from urllib.parse import parse_qs
from datetime import datetime
from connector import db_connector


FILE_PATH:  str = os.path.dirname(os.path.realpath(__file__))
PARENT_PATH:  str = os.path.abspath(os.path.join(FILE_PATH, os.pardir))

json_log:   str = 'db\\logger.json'
db_log:     str = 'db\\logtable.db'

json_log_path:str = os.path.join(PARENT_PATH, json_log)
db_log_path:str = os.path.join(PARENT_PATH, db_log)

HOST = 'localhost'
PORT = 8000


class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            default_login = "1149817"
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            html_content = f"""
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Форма</title>
            </head>
            <body>
                <form action="/" method="POST">
                    <label for="login">Логин:</label>
                    <input type="text" id="login" name="login" value="{default_login}" required><br>

                    <label for="time">Текущее время:</label>
                    <input type="text" id="time" name="time" value="{current_time}" readonly><br>

                    <button type="submit">Отправить</button>
                </form>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode("utf-8"))
        else:
            self.send_error(404, "Страница не найдена")

    def do_POST(self):
        if self.path == '/':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode("utf-8")
            form_data = parse_qs(post_data)
            
            login = form_data.get("login", [None])[0]
            current_time = form_data.get("time", [None])[0]
            
            if not login or not current_time:
                self.send_response(400)
                self.end_headers()

                self.wfile.write(b'Error: All fields are required')
                return
            
            # JSON
            data = {"login": login, "time": current_time}
            if os.path.exists(json_log_path):
                with open(json_log_path, "r", encoding="utf-8") as f:
                    try:
                        json_data = json.load(f)
                    except json.JSONDecodeError:
                        json_data = []
            else:
                json_data = []
            json_data.append(data)
            with open(json_log_path, "w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
            
            # SQLite
            connection = sqlite3.connect(db_log_path)
            with db_connector(connection) as con:
                con.execute("INSERT INTO users (login, time) VALUES (?, ?)", (login, current_time))
            
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            html_content = f"""
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Форма</title>
            </head>
            <body>
                <p>Данные успешно сохранены!</p>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode("utf-8"))
        else:
            self.send_error(404, "Page not found")


if __name__ == "__main__":
    server_address = (HOST, PORT)
    httpd = http.server.HTTPServer(server_address, SimpleHTTPRequestHandler)
    try:
        print(f"Server is live on http://{HOST}:{PORT}...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        print('Server stopped')
