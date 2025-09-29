# HTTPServer: 서버 자체를 담당하는 클래스
# 소켓을 열고 클라이언트 연결을 기다린 뒤, 요청이 들어오면 처리하는 역할
# BaseHTTPRequestHandler: 요청 처리용 핸들러 클래스
# GET, POST, PUT 등 HTTP 요청이 들어왔을 때 처리하는 메서드(do_GET, do_POST)를 정의 가능
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

#BaseHTTPRequestHandler 상속받아 SimpleHTTPRequestHandler 정의
# 클라이언트가 GET 요청을 보내면 자동으로 호출됨
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 200 OK 응답
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        # index.html 파일 읽어서 전송
        try:
            with open('index.html', 'r', encoding='utf-8') as file:
                html_content = file.read()
                self.wfile.write(html_content.encode('utf-8'))
        except FileNotFoundError:
            self.wfile.write('<h1>index.html 파일이 없습니다.</h1>'.encode('utf-8'))

        # 접속 정보 출력
        client_ip = self.client_address[0]
        access_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('접속 시간: {}, 클라이언트 IP: {}'.format(access_time, client_ip))


def run_server(host='0.0.0.0', port=8080):
    server_address = (host, port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print('웹 서버 시작: {}:{}'.format(host, port))
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
