import socket
import ssl 
from io import StringIO 

class URL:
    def __init__(self, url=None):
        if url == None:
            self.scheme = "file"
            self.host = "C:/test.html"
        else:
            self.scheme, url = url.split(":", 1)
            assert self.scheme in ["http", "https", "file", "data", "view-source"]

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
                if self.scheme == "http" or self.scheme == "view-source":
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
        # Check if page is already cached before making request
        with open("cache.txt", "r") as file:
            cached_html = ""
            cache_hit = False
            for ind, line in enumerate(file,0):
                if f"{self.host}{self.path}" in line:
                    #print("Cache hit")
                    cache_hit = True 
                elif f"{'-' * 10}" in line:
                    cache_hit = False 
                if cache_hit and f"{'*' * 10}" not in line:
                    cached_html += line 
            
            if cached_html != "":
                return ("200", cached_html)
            
            

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
        #request += "Connection: close\r\n"
        request += "Connection: keep-alive\r\n"
        request += "User-Agent: TristachoBrowser\r\n"
        request += "\r\n"
        s.send(request.encode("utf8"))

        # Read the bits as they come in response
        response = s.makefile("rb", encoding="utf8", newline="\r\n")
        statusline = response.readline().decode('utf-8')
        version, status, explanation = statusline.split(" ", 2)

        response_headers = {}
        while True:
            line = response.readline().decode('utf-8')
            if line == "\r\n": break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()

        if int(status) >= 300 and int(status) < 400:
            print(response_headers)
            return (status, response_headers['location'])
        
        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers
       

        content = response.read(int(response_headers['content-length'])).decode('utf-8')
        #s.close()
        if self.scheme in ['http', 'https']:
            self.cache_page(content)        
        
        return (status, content)
    
    def cache_page(self, content):
        tmp = StringIO()

        tmp.write(f"{self.host}{self.path}")
        tmp.seek(0,2)
        tmp.write(f"\n{'*' * 10}\n")
        tmp.seek(0, 2)
        tmp.write(content)
        tmp.seek(0,2)
        tmp.write(f"\n{'-'*10}")
        tmp.seek(0)

        file = open("cache.txt", "a")
        file.write(tmp.getvalue())
    
    