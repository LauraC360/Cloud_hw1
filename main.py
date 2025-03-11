import json
import http.server
import urllib
from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector

DB_CONFIG = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'tema1'
}

TABLE_NAME = "books"

def init_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            year INT NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# class RequestHandler(BaseHTTPRequestHandler):
#     def _set_headers(self, status_code=200):
#         self.send_response(status_code)
#         self.send_header('Content-type', 'application/json')
#         self.end_headers()
#
#     def do_GET(self):
#         conn = mysql.connector.connect(**DB_CONFIG)
#         cursor = conn.cursor()
#
#         route_args = self.path.strip("/").split("/")
#         response = {"error": "Internal server error"}
#         status = 500
#
#         if len(route_args) == 2 and route_args[0] == "books":
#             book_id = route_args[1]
#             cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = %s", (book_id,))
#             row = cursor.fetchone()
#
#             if row:
#                 response = {"id": row[0], "title": row[1], "author": row[2], "year": row[3]}
#                 status = 200
#             else:
#                 response = {"error": "Book not found"}
#                 status = 404
#
#         elif len(route_args) == 1 and route_args[0] == "books":
#             cursor.execute(f"SELECT * FROM {TABLE_NAME}")
#             rows = cursor.fetchall()
#
#             response = [{"id": row[0], "title": row[1], "author": row[2], "year": row[3]} for row in rows]
#             status = 200
#
#         else:
#             response = {"error": "Bad request. Bad route"}
#             status = 400
#
#         cursor.close()
#         conn.close()
#         self._set_headers(status)
#         self.wfile.write(json.dumps(response).encode())
#
#     def do_POST(self):
#         conn = mysql.connector.connect(**DB_CONFIG)
#         cursor = conn.cursor()
#
#         content_length = int(self.headers["Content-Length"])
#         post_data = json.loads(self.rfile.read(content_length))
#
#         route_args = self.path.strip("/").split("/")
#         response = {"error": "Internal server error"}
#         status = 500
#
#         if len(route_args) == 1 and route_args[0] == "books":
#             if "title" not in post_data or "author" not in post_data or "year" not in post_data:
#                 response = {"error": "Bad request. Bad content"}
#                 status = 400
#             else:
#                 title, author, year = post_data["title"], post_data["author"], post_data["year"]
#                 cursor.execute(f"INSERT INTO {TABLE_NAME} (title, author, year) VALUES (%s, %s, %s)", (title, author, year))
#                 conn.commit()
#                 response = {"message": "Created new book", "id": cursor.lastrowid}
#                 status = 201
#
#         else:
#             response = {"error": "Bad request. Bad route"}
#             status = 400
#
#         cursor.close()
#         conn.close()
#         self._set_headers(status)
#         self.wfile.write(json.dumps(response).encode())
#
#     def do_PUT(self):
#         conn = mysql.connector.connect(**DB_CONFIG)
#         cursor = conn.cursor()
#
#         content_length = int(self.headers["Content-Length"])
#         put_data = json.loads(self.rfile.read(content_length))
#
#         route_args = self.path.strip("/").split("/")
#         response = {"error": "Internal server error"}
#         status = 500
#
#         if len(route_args) == 2 and route_args[0] == "books":
#             book_id = route_args[1]
#             if "title" not in put_data or "author" not in put_data or "year" not in put_data:
#                 response = {"error": "Bad request. Bad content"}
#                 status = 400
#             else:
#                 title, author, year = put_data["title"], put_data["author"], put_data["year"]
#                 cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = %s", (book_id,))
#                 row = cursor.fetchone()
#
#                 if row:
#                     cursor.execute(f"UPDATE {TABLE_NAME} SET title = %s, author = %s, year = %s WHERE id = %s", (title, author, year, book_id))
#                     conn.commit()
#                     response = {"message": "Updated book"}
#                     status = 200
#                 else:
#                     response = {"error": "Book not found"}
#                     status = 404
#
#         else:
#             response = {"error": "Bad request. Bad route"}
#             status = 400
#
#         cursor.close()
#         conn.close()
#         self._set_headers(status)
#         self.wfile.write(json.dumps(response).encode())
#
#     def do_DELETE(self):
#         conn = mysql.connector.connect(**DB_CONFIG)
#         cursor = conn.cursor()
#
#         route_args = self.path.strip("/").split("/")
#         response = {"error": "Internal server error"}
#         status = 500
#
#         if len(route_args) == 2 and route_args[0] == "books":
#             book_id = route_args[1]
#             cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = %s", (book_id,))
#             row = cursor.fetchone()
#
#             if row:
#                 cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id = %s", (book_id,))
#                 conn.commit()
#                 response = {"message": "Deleted book"}
#                 status = 200
#             else:
#                 response = {"error": "Book not found"}
#                 status = 404
#
#         else:
#             response = {"error": "Bad request. Bad route"}
#             status = 400
#
#         cursor.close()
#         conn.close()
#         self._set_headers(status)
#         self.wfile.write(json.dumps(response).encode())

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        route_args = self.path.strip("/").split("/")
        response = {"error": "Internal server error"}
        status = 500

        if len(route_args) == 2 and route_args[0] == "books":
            book_id = route_args[1]
            cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = %s", (book_id,))
            row = cursor.fetchone()

            if row:
                response = {"id": row[0], "title": row[1], "author": row[2], "year": row[3]}
                status = 200
            else:
                response = {"error": "Book not found"}
                status = 404

        elif len(route_args) == 1 and route_args[0] == "books":
            cursor.execute(f"SELECT * FROM {TABLE_NAME}")
            rows = cursor.fetchall()

            response = [{"id": row[0], "title": row[1], "author": row[2], "year": row[3]} for row in rows]
            status = 200

        elif len(route_args) == 3 and route_args[0] == "books" and route_args[1] == "author":
            author_name = urllib.parse.unquote(route_args[2])
            cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE author = %s", (author_name,))
            rows = cursor.fetchall()

            response = [{"id": row[0], "title": row[1], "author": row[2], "year": row[3]} for row in rows]
            status = 200

        else:
            response = {"error": "Bad request. Bad route"}
            status = 400

        cursor.close()
        conn.close()
        self._set_headers(status)
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        content_length = int(self.headers["Content-Length"])
        post_data = json.loads(self.rfile.read(content_length))

        route_args = self.path.strip("/").split("/")
        response = {"error": "Internal server error"}
        status = 500

        if len(route_args) == 1 and route_args[0] == "books":
            if "title" not in post_data or "author" not in post_data or "year" not in post_data:
                response = {"error": "Bad request. Bad content"}
                status = 400
            else:
                title, author, year = post_data["title"], post_data["author"], post_data["year"]
                cursor.execute(f"INSERT INTO {TABLE_NAME} (title, author, year) VALUES (%s, %s, %s)", (title, author, year))
                conn.commit()
                response = {"message": "Created new book", "id": cursor.lastrowid}
                status = 201

        elif len(route_args) == 2 and route_args[0] == "books" and route_args[1] == "batch":
            if not isinstance(post_data, list):
                response = {"error": "Bad request. Bad content"}
                status = 400
            else:
                for book in post_data:
                    if "title" not in book or "author" not in book or "year" not in book:
                        response = {"error": "Bad request. Bad content"}
                        status = 400
                        break
                else:
                    for book in post_data:
                        cursor.execute(f"INSERT INTO {TABLE_NAME} (title, author, year) VALUES (%s, %s, %s)", (book["title"], book["author"], book["year"]))
                    conn.commit()
                    response = {"message": "Created new books"}
                    status = 201

        else:
            response = {"error": "Bad request. Bad route"}
            status = 400

        cursor.close()
        conn.close()
        self._set_headers(status)
        self.wfile.write(json.dumps(response).encode())

    def do_PUT(self):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        content_length = int(self.headers["Content-Length"])
        put_data = json.loads(self.rfile.read(content_length))

        route_args = self.path.strip("/").split("/")
        response = {"error": "Internal server error"}
        status = 500

        if len(route_args) == 2 and route_args[0] == "books" and route_args[1] == "batch":
            if not isinstance(put_data, list):
                response = {"error": "Bad request. Bad content"}
                status = 400
            else:
                for book in put_data:
                    if "id" not in book or "title" not in book or "author" not in book or "year" not in book:
                        response = {"error": "Bad request. Bad content"}
                        status = 400
                        break
                else:
                    for book in put_data:
                        cursor.execute(f"UPDATE {TABLE_NAME} SET title = %s, author = %s, year = %s WHERE id = %s", (book["title"], book["author"], book["year"], book["id"]))
                    conn.commit()
                    response = {"message": "Updated books"}
                    status = 200

        else:
            response = {"error": "Bad request. Bad route"}
            status = 400

        cursor.close()
        conn.close()
        self._set_headers(status)
        self.wfile.write(json.dumps(response).encode())

    def do_DELETE(self):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        route_args = self.path.strip("/").split("/")
        response = {"error": "Internal server error"}
        status = 500

        if len(route_args) == 2 and route_args[0] == "books":
            book_id = route_args[1]
            cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = %s", (book_id,))
            row = cursor.fetchone()

            if row:
                cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id = %s", (book_id,))
                conn.commit()
                response = {"message": "Deleted book"}
                status = 200
            else:
                response = {"error": "Book not found"}
                status = 404

        elif len(route_args) == 3 and route_args[0] == "books" and route_args[1] == "author":
            author_name = urllib.parse.unquote(route_args[2])
            cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE author = %s", (author_name,))
            conn.commit()
            response = {"message": "Deleted books by author"}
            status = 200

        else:
            response = {"error": "Bad request. Bad route"}
            status = 400

        cursor.close()
        conn.close()
        self._set_headers(status)
        self.wfile.write(json.dumps(response).encode())

    def do_PATCH(self):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        content_length = int(self.headers["Content-Length"])
        patch_data = json.loads(self.rfile.read(content_length))

        route_args = self.path.strip("/").split("/")
        response = {"error": "Internal server error"}
        status = 500

        if len(route_args) == 3 and route_args[0] == "books":
            book_id = route_args[1]
            field = route_args[2]

            if field == "title" and "title" in patch_data:
                cursor.execute(f"UPDATE {TABLE_NAME} SET title = %s WHERE id = %s", (patch_data["title"], book_id))
                conn.commit()
                response = {"message": "Updated book title"}
                status = 200
            elif field == "author" and "author" in patch_data:
                cursor.execute(f"UPDATE {TABLE_NAME} SET author = %s WHERE id = %s", (patch_data["author"], book_id))
                conn.commit()
                response = {"message": "Updated book author"}
                status = 200
            else:
                response = {"error": "Bad request. Bad content"}
                status = 400

        else:
            response = {"error": "Bad request. Bad route"}
            status = 400

        cursor.close()
        conn.close()
        self._set_headers(status)
        self.wfile.write(json.dumps(response).encode())

    def do_HEAD(self):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        route_args = self.path.strip("/").split("/")
        status = 500

        if len(route_args) == 2 and route_args[0] == "books":
            book_id = route_args[1]
            cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = %s", (book_id,))
            row = cursor.fetchone()
            status = 200 if row else 404

        elif len(route_args) == 3 and route_args[0] == "books" and route_args[1] == "author":
            author_name = urllib.parse.unquote(route_args[2])
            cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE author = %s", (author_name,))
            row = cursor.fetchone()
            status = 200 if row else 404

        else:
            status = 400

        cursor.close()
        conn.close()
        self._set_headers(status)

    def do_OPTIONS(self):
        route_args = self.path.strip("/").split("/")
        response = {}

        if len(route_args) == 1 and route_args[0] == "books":
            self.send_response(200)
            self.send_header('Allow', 'GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS')
            response = {"methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]}
        elif len(route_args) == 2 and route_args[0] == "books":
            self.send_response(200)
            self.send_header('Allow', 'GET, PUT, DELETE, PATCH, HEAD, OPTIONS')
            response = {"methods": ["GET", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]}
        elif len(route_args) == 3 and route_args[0] == "books" and route_args[1] == "author":
            self.send_response(200)
            self.send_header('Allow', 'GET, DELETE, HEAD, OPTIONS')
            response = {"methods": ["GET", "DELETE", "HEAD", "OPTIONS"]}
        else:
            self.send_response(400)
            response = {"error": "Bad request. Bad route"}

        self.end_headers()
        self.wfile.write(json.dumps(response).encode())


if __name__ == "__main__":
    # Test + Database initialization
    #init_db()

    server_address = ("", 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Starting server on port 8000...")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()