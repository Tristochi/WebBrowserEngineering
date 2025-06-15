from url import *

def show(body, scheme):
    in_tag = False
    entity = False
    entity_str = ""
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif c == "&":
            entity = True 
        elif c == ";":
            entity_str += c
            entity = False 
            if entity_str == "&lt;":
                c = "<"
            elif entity_str == "&gt;":
                c=">"
            print(entity_str)
        elif not in_tag and not entity and scheme != "view-source":
            print(c, end="")
            entity_str = ""
        
        if scheme == "view-source": 
            print(c, end="")
            entity_str = ""
        
        if entity:
            entity_str += c


            

def load(url):
    if url.get_scheme() == "file":
        show(url.open_file())
    elif url.get_scheme() == "data":
        show(url.get_body())
    else:
        body = url.request()
        scheme = url.get_scheme()
        print(f"Scheme: {scheme}")
        show(body, scheme)

# This allows us to run the file from the command line
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        load(URL(sys.argv[1]))
    else:
        url = URL()
        scheme = url.get_scheme()
        show(url.open_file(), scheme)
