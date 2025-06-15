from url import *

def show(body):
    in_tag = False
    entity = False
    entity_str = ""
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        
        if entity:
            entity_str += c
        if c == "&":
            entity = True
            entity_str += c
        elif c == ";":
            entity = False
            if entity_str == "&lt;":
                c = "<"
            elif entity_str == "&gt;":
                c = ">"
        if not in_tag and not entity:
            print(c, end="")
            entity_str = ""
            

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
