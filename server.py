import http.server
import socketserver

PORT = 8765

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """多线程 HTTP 服务器，支持多个浏览器同时访问。"""
    daemon_threads = True

with ThreadingHTTPServer(("", PORT), NoCacheHandler) as httpd:
    print(f"笔记本服务器已启动: http://localhost:{PORT} (缓存已禁用)")
    httpd.serve_forever()