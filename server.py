import BaseHTTPServer
import urlparse
import psycopg2
import os
import sys

class SimpleHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        if "?" in self.path and "addQuery" in self.path:
            queryString = "https://www.yad2.co.il/api/pre-load/getFeedIndex/realestate/rent?";

            for key,value in dict(urlparse.parse_qsl(self.path.split("?")[1], True)).items():
                print(key + " = " + value)
                if value:
                    queryString+= "&" + key + "=" + value

            try:
                DATABASE_URL = os.environ['DATABASE_URL']
                conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO queries(user_id, query) VALUES('623781198','" +queryString+"')")
                htmlResponse = "inserted: " + queryString
                conn.commit()
                print("Record inserted successfully into python_users table")

            except (Exception, psycopg2.Error) as error:
                print("Error connecting or inserting to PostgreSQL", error)
                htmlResponse = "error with data insert "
                sys.exit("Error connecting or inserting to PostgreSQL")
        else:
            htmlResponse = "no data inserted"

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write(htmlResponse)
        return

    def do_POST(self):
        self.send_response(200)
        if self.rfile:
             # print urlparse.parse_qs(self.rfile.read(int(self.headers['Content-Length'])))
             for key,value in dict(urlparse.parse_qs(self.rfile.read(int(self.headers['Content-Length'])))).items():
                 print(key + " = " + value[0])

    def log_request(self, code=None, size=None):
        return

if __name__ == "__main__":
    try:
        BaseHTTPServer.HTTPServer(("0.0.0.0", 5000), SimpleHandler).serve_forever()
    except KeyboardInterrupt:
        print('shutting down server')