import socket
import socketserver
import random, json

hostname = socket.gethostname()
ip_addresses = socket.getaddrinfo(hostname, None)

print("Текущие IP-адреса локального сервера:")
for address in ip_addresses:
    ip = address[4][0]
    print(f"\t{ip}")


from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = parsed_path.query

        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            # Нужно добавлять разрешения CORS, чтобы не блокировать получение ответов
            self.send_header('Access-Control-Allow-Method', 'GET')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'Hello, world!')
            
        elif path == '/json':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            
            # Нужно добавлять разрешения CORS, чтобы не блокировать получение ответов
            self.send_header('Access-Control-Allow-Method', 'GET')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            # генерируем случайное целое число от 0 до 100 и возвращаем его клиенту в формате JSON
            random_number = random.randint(0, 100)
            response_data = {'random_number': random_number , 'answer': random_number}
            self.wfile.write(json.dumps(response_data).encode())
       
        elif path == '/001':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Method', 'GET')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'print("hello world!")')
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Method', 'GET')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def log_message(self, format, *args):
        message = format % args
        print(f'Подключение: {self.client_address[0]} - {message}')

server_address = ('', 8000)
httpd = socketserver.ThreadingTCPServer(server_address, MyHandler)
httpd.serve_forever()
