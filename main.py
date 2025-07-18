from url import *
from browser import *

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18

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


def lex(body, scheme):
    text = ""
    
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
            text+=c
            entity_str = ""
        
        if scheme == "view-source": 
            text+=c
            entity_str = ""
        
        if entity:
            entity_str += c
    file = open("test.txt", "a",encoding="utf-8")
    for c in text: 
        file.write(c)
    return text 

def load(url):
    if url.get_scheme() == "file":
        show(url.open_file(), scheme="file")
    elif url.get_scheme() == "data":
        show(url.get_body(), scheme="data")
    else:
        response = url.request()
        if 300 <= int(response[0]) < 400:
            url = URL(response[1])
            for i in range(3):
                response = url.request()
                if not (300 <= int(response[0]) < 400):
                    break
            

        scheme = url.get_scheme()
        print(f"Scheme: {scheme}")
        lex(response[1], scheme)

def layout(text):
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP 

    for c in text:
        display_list.append((cursor_x, cursor_y, c))
        cursor_x += HSTEP
        if cursor_x >= WIDTH - HSTEP:
            cursor_y += VSTEP 
            cursor_x = HSTEP 
            
    return display_list 

# This allows us to run the file from the command line
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        Browser().load(URL(sys.argv[1]))
        tkinter.mainloop()
    else:
        url = URL()
        scheme = url.get_scheme()
        show(url.open_file(), scheme)

"""     if len(sys.argv) > 1:
        load(URL(sys.argv[1]))
    else:
        url = URL()
        scheme = url.get_scheme()
        show(url.open_file(), scheme) """

    
