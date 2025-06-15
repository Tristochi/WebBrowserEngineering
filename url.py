import socket
import ssl 

class URL:
    def __init__(self, url=None):
        if url == None:
            self.scheme = "file"
            self.host = "C:/test.html"
        else:
            self.scheme, url = url.split(":", 1)
            assert self.scheme in ["http", "https", "file", "data"]

            if self.scheme == "file":
                self.host = url[1:]
            elif self.scheme == "data":
                self.content_type, self.body = url.split(",", 1)     
            else:
                url = url.split("//",1)[1]
                if "/" not in url:
                    url = url + "/"
                self.host, url = url.split("/", 1)
                self.path = "/" + url

                # Encyrpted HTTP connections usually user port 443 instead of port 80
                if self.scheme == "http":
                    self.port = 80
                elif self.scheme == "https":
                    self.port = 443
                
                # Allow for custom ports
                if ":" in self.host:
                    self.host, port = self.host.split(":", 1)
                    self.port = int(port)
    
    def open_file(self):
        print(self.host)
        file = open(self.host, mode='r', encoding='utf8')
        file_content = file.read()

        return file_content

    def get_scheme(self):
        return self.scheme 

    def get_body(self):
        return self.body
    
    def request(self):
        # Define socket and establish a connection
        
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        s.connect((self.host, self.port))

        # If https wrap in default context to establish a secure connection for TLS
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)


        # Send some data using the send method
        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        request += "Connection: close\r\n"
        request += "User-Agent: TristachoBrowser\r\n"
        request += "\r\n"
        s.send(request.encode("utf8"))

        # Read the bits as they come in response
        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)

        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n": break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()

        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers

        content = response.read()
        s.close()

        return content
    
    