from url import *

def show(body):
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")

def load(url):
    if url.get_scheme() == "file":
        show(url.open_file())
    elif url.get_scheme() == "data":
        show(url.get_body())
    else:
        body = url.request()
        show(body)

# This allows us to run the file from the command line
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        load(URL(sys.argv[1]))
    else:
        url = URL()
        show(url.open_file())
