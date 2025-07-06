import tkinter 
from url import *
import main  

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100
class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.display_list = ""
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<MouseWheel>", self.scrollwheel)
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
            self.display_list = main.layout(text)
            self.draw()

    def draw(self):
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            # Avoid drawing characters that are not on screen to speed up the draw time.
            if y > self.scroll + HEIGHT: continue 
            if y + VSTEP < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=c)
    
    def scrolldown(self,e):
        last_x_pos, last_y_pos, c = self.display_list[-2]
        print(f"Current scroll: {self.scroll}, Scroll pos + scroll step: {self.scroll+SCROLL_STEP}, Last Y pos: {last_y_pos}")
        if last_y_pos - self.scroll > HEIGHT:
            self.scroll += SCROLL_STEP
            self.draw()
    
    def scrollup(self, e):
        if self.scroll > 0:
            self.scroll -= SCROLL_STEP 
            self.draw()
    
    def scrollwheel(self, e):
        if e.delta > 0:
            self.scrollup(e)
        else: 
            self.scrolldown(e)