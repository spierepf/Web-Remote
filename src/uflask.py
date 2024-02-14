from select import select

try:
    import logging
except:
    import ulogging as logging

try:
    import re
except:
    import ure as re

try:
    import socket
except:
    import usocket as socket

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('uflask')


class Flask:
    def __init__(self, micropython_optimize=False):
        self.micropython_optimize = micropython_optimize
        self.routes = []
        self.sock = self._make_socket()

    @staticmethod
    def _make_socket():
        s = socket.socket()

        # Binding to all interfaces - server will be accessible to other hosts!
        ai = socket.getaddrinfo("0.0.0.0", 8080)
        log.info(f"Bind address info: {ai}")
        addr = ai[0][-1]

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(5)
        log.info("Listening, connect your browser to http://<this_host>:8080/")
        return s

    def route(self, uri_pattern):
        return lambda handler: self.add_route(uri_pattern, handler)

    def add_route(self, uri_pattern, handler):
        self.routes += [(re.compile(uri_pattern), handler)]

    def find_handler(self, uri):
        for (uri_regex, handler) in self.routes:
            match = uri_regex.match(uri.decode('utf-8'))
            if match is not None:
                return lambda: handler(match)
        return None

    def write_to_stream(self, source, stream):
        t = str(type(source))
        if t == "<class 'str'>":
            stream.write(source.encode('utf-8'))
        elif t == "<class 'generator'>":
            for i in source:
                self.write_to_stream(i, stream)
        elif t == "<class 'NoneType'>":
            pass
        else:
            log.info(t)
            raise RuntimeError

    def handle(self, uri, stream):
        handler = self.find_handler(uri)
        if handler is None:
            stream.write(b"HTTP/1.1 404 NOT FOUND\r\n")
            stream.write(b"\r\n")
        else:
            stream.write(b"HTTP/1.1 200 OK\r\n")
            stream.write(b"\r\n")
            self.write_to_stream(handler(), stream)

    def handle_request(self):
        res = self.sock.accept()
        client_sock = res[0]
        client_addr = res[1]
        log.info(f"Client address: {client_addr}")
        log.info(f"Client socket: {client_sock}")

        if not self.micropython_optimize:
            # To read line-oriented protocol (like HTTP) from a socket (and
            # avoid short read problem), it must be wrapped in a stream (aka
            # file-like) object. That's how you do it in CPython:
            client_stream = client_sock.makefile("rwb")
        else:
            # .. but MicroPython socket objects support stream interface
            # directly, so calling .makefile() method is not required. If
            # you develop application which will run only on MicroPython,
            # especially on a resource-constrained embedded device, you
            # may take this shortcut to save resources.
            client_stream = client_sock

        request_line = client_stream.readline().strip().split(b" ")
        log.info(request_line)
        try:
            method = request_line[0]
            request_uri = request_line[1]
            http_version = request_line[2]

            headers = {}
            while True:
                h = client_stream.readline()
                if h == b"" or h == b"\r\n":
                    break
                header_line = h.strip().split(b": ", 1)
                headers[header_line[0]] = header_line[1]

            log.info(f"Method: {method}")
            log.info(f"Request: {request_uri}")
            log.info(f"Version: {http_version}")
            log.info(f"Headers: {headers}")

            self.handle(request_uri, client_stream)

            client_stream.close()
            if not self.micropython_optimize:
                client_sock.close()
            print()
        except:
            log.exception("Exception in main loop")
            log.error(f"While handling request {request_line}")

    def process_waiting_packets(self):
        # Handle all the packets that can be read immediately and
        # return as soon as none are waiting
        while True:
            readers, _, _ = select([self.sock], [], [], 0)
            if not readers:
                break
            else:
                self.handle_request()

    def run_forever(self):
        # Only really useful once we have stable thread support
        while True:
            readers, _, _ = select([self.sock], [], [], None)
            self.process_waiting_packets()
