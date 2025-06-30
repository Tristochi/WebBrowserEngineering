import tkinter 
from url import *
import main  

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack()

    def load(self, url):
        if url.get_scheme() == "file":
            text = main.lex(url.open_file(), scheme="file")
        elif url.get_scheme() == "data":
            text = main.lex(url.get_body(), scheme="data")
        else:
            response = url.request()
            if 300 <= int(response[0]) < 400:
                url = URL(response[1])
                for i in range(3):
                    response = url.request()
                    if not (300 <= int(response[0]) < 400):
                        break
                

            scheme = url.get_scheme()
            #print(f"Scheme: {scheme}")
            text = main.lex(response[1], scheme)
        
        #self.canvas.create_rectangle(10, 20, 400, 300)
        #self.canvas.create_oval(100, 100, 150, 150)
        #self.canvas.create_text(200, 150, text="Hi!")
        cursor_x, cursor_y = HSTEP, VSTEP 
        for c in text:
            self.canvas.create_text(cursor_x, cursor_y, text=c)
            cursor_x += HSTEP

            if cursor_x >= WIDTH - HSTEP:
                cursor_y += VSTEP 
                cursor_x = HSTEP 
        