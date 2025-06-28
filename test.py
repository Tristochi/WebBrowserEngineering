from io import BytesIO
import io 


def chunked_data(response):
    statusline = response.readline().decode('utf-8')
    response_headers = {}
    while True:
        line = response.readline().decode('utf-8')
        if line == "\r\n": break
        header, value = line.split(":", 1)
        response_headers[header.casefold()] = value.strip()
    print(response_headers)

    content = ""
    while True:
                length = response.readline().decode('utf-8').strip()
                try:
                    length = int(length,16)
                except:
                    continue 

                if length == 0:
                    break 

                chunked_data = response.read(length).decode('utf-8')
                response.read(2)
                content += chunked_data + " "
    return content 

text = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/plain\r\n"
    "Transfer-Encoding: chunked\r\n"
    "\r\n"
    "7\r\n"
    "Mozilla\r\n"
    "11\r\n"
    "Developer Network\r\n"
    "0\r\n"
    "\r\n"
)

response = BytesIO(text.encode('utf-8'))
#response = io.TextIOWrapper(response, encoding='utf-8', newline='\r\n')

print(chunked_data(response))

