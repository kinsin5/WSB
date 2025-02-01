from dpi import set_dpi_awareness
#from window1 import *
from window2 import *

set_dpi_awareness()

class SmallCommander(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Small Commander")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=4)
        self.columnconfigure(4, weight=1)
        self.rowconfigure(0, weight=1)

        frame1 = Window_1(self)
        frame1.grid(row=0, column=1, sticky="NSEW")
      
        frame2 = Window_2(self)
        frame2.grid(row=0, column=3, sticky="NSEW")

        separator = ttk.Separator(orient="vertical")
        separator.grid(column=2, row=0, sticky="NS")

        #KEYBOARD BINDING TO frame1 and frame2
        self.bind("<F7>", frame1.on_create_shortcut)  # F7 for create folder in Window 1
        self.bind("<F8>", frame1.on_delete_shortcut)  # F8 for delete in Window 1
        self.bind("<F5>", frame2.on_create_shortcut)  # F5 for create folder in Window 2
        self.bind("<F6>", frame2.on_delete_shortcut)  # F6 for delete in Window 2

        self.center_app()

    def center_app(self):

        screen_width = round(self.winfo_screenwidth() // 1.5)
        screen_height = round(self.winfo_screenheight() // 1.5)
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()
        print(window_height, window_width)
        x = (window_width) + 100
        y = (window_height) - 50
        self.geometry(f"{screen_width}x{screen_height}+{x}+{y}")
        

class Window_2(Window_1):  # Window_2 dziedziczy po Window_1, musimy w niej wprowadzić tylko pewne modyfikacja
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.short1 = ttk.Label(self, text="[F6]")
        self.short2 = ttk.Label(self, text="[F5]")

        self.short1.grid(column=0, row=4, sticky="")
        self.short2.grid(column=1, row=4, columnspan=2, sticky="")
        


if __name__ == "__main__":
    
    app = SmallCommander()
    # app.geometry(app.center_app())
    app.mainloop()

#LOCKING IS COMPLETE NOW GET RID OF VISUAL EFFECT OF HIGHLITHING ITEM IN LIST CUZ IT MISSLEADING
