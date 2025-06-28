import socket
import ssl 
from io import StringIO 
import gzip

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
        with open("cache.txt", mode="r", encoding="utf-8") as file:
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
        request += "Accept-Encoding: gzip\r\n"
        request += "\r\n"
        s.send(request.encode("utf8"))

        # Read the bits as they come in response
        response = s.makefile("rb", encoding="utf-8", newline="\r\n")
        statusline = response.readline().decode('utf-8')

        version, status, explanation = statusline.split(" ", 2)

        response_headers = {}
        while True:
            line = response.readline().decode('utf-8')
            if line == "\r\n": break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()

        print(f"Response Headers: {response_headers}")

        if int(status) >= 300 and int(status) < 400:
            print(response_headers)
            return (status, response_headers['location'])
        

        #assert "content-encoding" not in response_headers
        if "content-encoding" in response_headers:
            #print(f"Content-encoding: {response_headers['content-encoding']}")
            if response_headers['content-encoding'] == "gzip":
                if "transfer-encoding" in response_headers:
                    transfer_encoding = response_headers['transfer-encoding'].split(",")
                    if "chunked" in transfer_encoding:
                        #Typically the content-encoding is applied before the transfer-encoding so I need to decompress
                        #but I will have to get each chunk, append together, then decompress. 
                        #Chunk length is specified by a hex num at the beginning of each chunk. The last chunk has 0 at the beginning. 
                        while True:
                            length = response.readline().decode("utf-8").strip()
                            try:
                                length = int(length,16)
                            except:
                                continue 

                            if length == 0:
                                break 

                            chunked_data = response.read(length)
                            response.read(2)
                            content += chunked_data
                        
                        content = gzip.decompress(content.decode('utf-8'))
                            
                else:
                    content = gzip.decompress(response.read(int(response_headers['content-length']))).decode('utf-8')
        elif "transfer-encoding" in response_headers and "content-encoding" not in response_headers:
            while True:
                length = response.readline().decode("utf-8").strip()
                try:
                    length = int(length,16)
                except:
                    continue 

                if length == 0:
                    break 

                chunked_data = response.read(length).decode('utf-8')
                response.read(2)
                content += chunked_data
            
        else:
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
        tmp.write(f"\n{'-'*10}\n")
        tmp.seek(0)

        file = open(file="cache.txt", encoding="utf-8",mode="a")
        file.write(tmp.getvalue())
    
    