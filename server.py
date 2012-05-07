import os
try:
    import BaseHTTPServer
except ImportError:
    import http.server as BaseHTTPServer
try:
    from SimpleHTTPServer import SimpleHTTPRequestHandler
except ImportError:
    from http.server import SimpleHTTPRequestHandler
from .core import logger

def simple_server(ip = '127.0.0.1', port = 8000, path = None):
    if path is not None:
        os.chdir(path)

    HandlerClass = SimpleHTTPRequestHandler
    ServerClass  = BaseHTTPServer.HTTPServer
    Protocol     = "HTTP/1.0"
    server_address = (ip, port)

    HandlerClass.protocol_version = Protocol
    httpd = ServerClass(server_address, HandlerClass)

    sa = httpd.socket.getsockname()
    logger.info('start simple server on %s:%s...' % (sa[0], sa[1]))
    httpd.serve_forever()