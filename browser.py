from tkinter import *
from tkinter import ttk
from url import *
import main  

class Browser:
    def __init__(self):
        self._WIDTH = 800
        self._HEIGHT = 600
        self._HSTEP = 13
        self._VSTEP = 18
        self._SCROLL_STEP = 100
        self.window = Tk()
        self.display_list = [[self._WIDTH,self._HEIGHT,""]]
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<MouseWheel>", self.scrollwheel)
        self.window.bind("<Configure>", self.resize)
        
        self.canvas = Canvas(
            self.window,
            width=self._WIDTH,
            height=self._HEIGHT,
            scrollregion=(0, 0, self.display_list[-1][1], self._WIDTH)
        )
        self.style = ttk.Style(self.window)
        self.style.theme_use("default")
        self.style.configure("Blue.Vertical.TScrollbar",
                             background="blue",
                             troughcolor="lightblue",
                             arrowcolor="white")
        self.scrollbar = ttk.Scrollbar(self.window, orient=VERTICAL, command=self.canvas.yview,style="Blue.Vertical.TScrollbar")

        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT,fill=Y)
        self.canvas.pack(side=LEFT,fill=BOTH, expand=1)
        
        self.text = ""
    
    def canvas_config(self, e):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def resize(self, e):
        self._HEIGHT = e.height
        self._WIDTH = e.width
        self.display_list = main.layout(self.text, width=e.width, height=e.height)

        self.draw()

    def load(self, url):
        if url.get_scheme() == "file":
            self.text = main.lex(url.open_file(), scheme="file")
        elif url.get_scheme() == "data":
            self.text = main.lex(url.get_body(), scheme="data")
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
            self.text = main.lex(response[1], scheme)
            self.display_list = main.layout(self.text)
            self.draw()

    def draw(self):
        self.canvas.delete("all")

        for x, y, c in self.display_list:
            # Avoid drawing characters that are not on screen to speed up the draw time.
            #if y > self.scroll + self._HEIGHT: continue 
            #if y + self._VSTEP < self.scroll: continue
            #self.canvas.create_text(x, y - self.scroll, text=c)
            self.canvas.create_text(x,y,text=c)
        
        width, self._HEIGHT, c = self.display_list[-1]
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def scrolldown(self,e):
        last_x_pos, last_y_pos, c = self.display_list[-2]
        #print(f"Current scroll: {self.scroll}, Scroll pos + scroll step: {self.scroll+self._SCROLL_STEP}, Last Y pos: {last_y_pos}")
        #if last_y_pos - self.scroll > self._HEIGHT:
        #self.scroll += self._SCROLL_STEP
        self.canvas.yview_scroll(int(-1*(e.delta/120)), "units")
            #self.draw()
    
    def scrollup(self, e):
        self.canvas.yview_scroll(int(-1*(e.delta/120)), "units")
        #if self.scroll > 0:
            #self.scroll -= self._SCROLL_STEP 
            
            #self.draw()
    
    def scrollwheel(self, e):
        if e.delta > 0:
            self.scrollup(e)
        else: 
            self.scrolldown(e)