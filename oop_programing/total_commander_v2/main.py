from dpi import set_dpi_awareness
from window import *

set_dpi_awareness()

class SmallCommander(tk.Tk): #Główna klasa w której inicjalizujmey okna oraz nadpisujemy tkinter
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # init z klasu Tk
        #wstępna konfiguracja kolumn w której umieszczamy nasze okna i seperatory
        self.title("Small Commander")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=4)
        self.columnconfigure(4, weight=1)
        self.rowconfigure(0, weight=1)
        #tworzenie obiektów typu ttk.Frame które nadpisaliśmy w naszej klasie Window
        frame1 = Window_1(self)
        frame1.grid(row=0, column=1, sticky="NSEW")
      
        frame2 = Window_2(self)
        frame2.grid(row=0, column=3, sticky="NSEW")

        separator = ttk.Separator(orient="vertical")
        separator.grid(column=2, row=0, sticky="NS")

        #KEYBOARD BINDING do tworzenia i usuwania plików/folderów
        self.bind("<F7>", frame1.on_create_shortcut)  # F7 tworzenie w Window 1
        self.bind("<F8>", frame1.on_delete_shortcut)  # F8 usuwanie w  Window 1
        self.bind("<F5>", frame2.on_create_shortcut)  # F5 tworzenie w Window 2
        self.bind("<F6>", frame2.on_delete_shortcut)  # F6 usuwanie Window 2

        self.center_app()

    def center_app(self): #metoda do wyśrodkowania aplikacji

        screen_width = round(self.winfo_screenwidth() // 1.5)
        screen_height = round(self.winfo_screenheight() // 1.5)
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()
        #print(window_height, window_width)
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
        
if __name__ == "__main__": # main
    
    #Tworzenie obiektu SmallCommander zmiana jest stylu oraz uruchomienie głównego okna

    app = SmallCommander()
    style = ttk.Style(app)
    style.theme_use("vista")

    app.mainloop()


#TODO:
#LOCKING IS COMPLETE NOW GET RID OF VISUAL EFFECT OF HIGHLITHING ITEM IN LIST CUZ IT MISSLEADING 
