import tkinter as tk
from tkinter import ttk
import os
import time
import shutil #do przenoszenia plików


class Window_1(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.current_dir = tk.StringVar(value=os.getcwd())  # Pobieramy początkową ścieżkę
        self.list_value = tk.StringVar(value=[]) # puste listy
        self.date_value = tk.StringVar(value=[])
        self.dragged_item = None  # Przenoszny plik
        self.source_frame = None  # Window z którego pobieramy plik
        self.drag_start_flag = False  # Rozpoczęcie przeciągania
        # Konfiguracja kolumn w środku naszego okna
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=10)
        self.rowconfigure(3, weight=2)

        # Kompententy które umieścimy w UI w raz z połączeniem do odpowiednich metod
        self.dir_label = ttk.Label(self, textvariable=self.current_dir)
        self.parent_button = ttk.Button(self, text="Parent Folder", command=self.go_to_parent)
        self.files_list = tk.Listbox(self, listvariable=self.list_value)
        self.date_list = tk.Listbox(self, listvariable=self.date_value)
        self.sort_name_button = ttk.Button(self, text="Sort by Name", command=self.sort_by_name)
        self.sort_date_button = ttk.Button(self, text="Sort by Date", command=self.sort_by_date)
        self.delete_button = ttk.Button(self, text="Delete", command=self.delete_item)
        self.create_button = ttk.Button(self, text="Create Folder", command=self.create_folder)
        self.short1 = ttk.Label(self, text="[F8]")
        self.short2 = ttk.Label(self, text="[F7]")
        
        #### Layout
        self.dir_label.grid(column=0, row=0, columnspan=2, sticky="N")
        self.parent_button.grid(column=0, row=1, sticky="EW")
        self.sort_name_button.grid(column=1, row=1, sticky="EW")
        self.sort_date_button.grid(column=2, row=1, sticky="EW")

        for child in self.winfo_children():
            child.grid_configure(padx=8, pady=8)
        self.files_list.grid_configure(padx=0)
        self.date_list.grid_configure(padx=0)
        
        self.delete_button.grid(column=0, row=3, sticky="")
        self.create_button.grid(column=1, row=3, columnspan=2, sticky="")
        self.files_list.grid(column=0, row=2, sticky="NSWE")
        self.date_list.grid(column=1, row=2, columnspan=2, sticky="NSWE")
        self.short1.grid(column=0, row=4, sticky="N")
        self.short2.grid(column=1, row=4, columnspan=2, sticky="N")
        ###

        # Pobieramy liste plików znajdującą się w obecnej ścieżce
        self.update_directory_contents(self.current_dir.get())

        # Bind podwojnego klikniecia
        self.files_list.bind("<Double-1>", self.on_item_double_click) 

        # Bind i śledzenie drag and drop
        self.selected_item = None
        self.files_list.bind("<<ListboxSelect>>", self.on_listbox_select)
        self.files_list.bind("<ButtonPress-1>", self.on_drag_start)
        self.files_list.bind("<B1-Motion>", self.on_drag_motion)
        self.files_list.bind("<ButtonRelease-1>", self.on_drop)

    def update_directory_contents(self, path): # uzupełnianie listy plików oraz ich czasów stworzenia.
        """Update the listbox to show the contents of the directory."""
        try:
            items = os.listdir(path)
            items = [os.path.abspath(path)] + items if path != os.path.abspath(path) else items # pomijanie absolute path
            self.list_value.set(items)
            self.date_value.set([time.ctime(os.path.getctime(os.path.join(path, item))) for item in items]) # populacja listy czasów stworzenia plików list comprehension
            self.current_dir.set(path)
        except Exception as e:
            print(f"Error loading directory {path}: {e}")

    def go_to_parent(self): # przejście do nadrzędnego folderu pobierając dirname(path)
        current_path = self.current_dir.get()
        new_path = os.path.dirname(current_path)
        self.update_directory_contents(new_path)

    def sort_by_name(self): # Sortowanie po nazwie case insensitive
        current_path = self.current_dir.get()
        items = os.listdir(current_path)
        items.sort(key=lambda item: item.lower())  # sortowanie listy od a do z 
        self.list_value.set(items) 
        self.date_value.set([time.ctime(os.path.getctime(os.path.join(current_path, item))) for item in items]) #list comp do stworzenia na nowo czasów dla postrtowanej listy

    def sort_by_date(self): # Sortowanie od najnowszego pliku do najstarszego
        current_path = self.current_dir.get()
        items = os.listdir(current_path)
        items.sort(key=lambda item: os.path.getctime(os.path.join(current_path, item)), reverse=True) #bez resverse=True od najstarszych
        self.list_value.set(items)
        self.date_value.set([time.ctime(os.path.getctime(os.path.join(current_path, item))) for item in items])

    def delete_item(self): # Usuwanie pliku lub folderu
        if self.selected_item is None:  # Najpierw musimy mieć sprawdzony atrybut czy list jest selected
            print("No item selected") 
            return

        current_path = self.current_dir.get()
        path_to_delete = os.path.join(current_path, self.selected_item) # Otrzymujemy sciezke z plikiem do usuniecia

        try:
            if os.path.isdir(path_to_delete): #W zależności czy to folder/plik os.rmdir lub os.remove
                os.rmdir(path_to_delete)
            else:
                os.remove(path_to_delete)
            self.update_directory_contents(current_path) #update obecnego stanu folderu
        except Exception as e:
            print(f"Error deleting {path_to_delete}: {e}")

    def create_folder(self): # Tworzenie nowego folderu w obecnej ścieżce
        current_path = self.current_dir.get()
        # Popup po inicjalizacji metody

        popup = tk.Toplevel(self)
        popup.title("Create New Folder")

        # Wyśrodkowanie popupu
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        window_width = popup.winfo_reqwidth()
        window_height = popup.winfo_reqheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        popup.geometry(f"{window_width}x{window_height - 100}+{x}+{y}")

        # prosty tk.Entry do wpisania nazwy folderu
        folder_name_entry = tk.Entry(popup)
        folder_name_entry.pack(padx=10, pady=10)

        # zagnieżdżona metoda do tworzenia folderu
        def confirm_create():
            folder_name = folder_name_entry.get()
            if folder_name: #jezeli nie pusty to:
                folder_path = os.path.join(current_path, folder_name)
                try:
                    os.mkdir(folder_path) #tworzmy folder przekazujac sciezke do mkdir
                    self.update_directory_contents(current_path)
                    popup.destroy()  # zamykanie popupu
                except Exception as e:
                    print(f"Error!!{folder_path}: {e}")
            else:
                print("Folder name must be specifed!")
        # Button z metoda confirm_create  
        confirm_button = tk.Button(popup, text="Create", command=confirm_create)
        confirm_button.pack(padx=10, pady=10)

    def on_delete_shortcut(self, event): # wywoływanie metody za pomoca przycisku F8
        self.delete_item()

    def on_create_shortcut(self, event): # wywoływanie metody za pomoca przycisku F7
        self.create_folder()

    def on_listbox_select(self, event): # Sledzenie wybranego pliku/folderu w listboxie
        selection = self.files_list.get(self.files_list.curselection())
        self.selected_item = selection
        print(f"Selected item: {self.selected_item}") # consolowe sprawdzanie programu
    
    def on_drag_start(self, event): #Start dragowania z opóznienie aby również można korzystać z double-click do przenoszenia do folderów
        self.drag_start_flag = True  # ustawianie drag flag
        self.after(200, self._start_drag, event)  # opoznienie

    def _start_drag(self, event): #Blokowanie pliku/folderu po starcie przenoszenia
        if self.drag_start_flag:
            try:
                index = self.files_list.nearest(event.y) # lock pliku
                self.dragged_item_index = index  # lock indeksu przenoszenego pliku
                self.dragged_item = self.files_list.get(index)  # lock nazwy przenoszeonego pliku
                self.source_frame = self
                # TODOTODO!! Zaznaczenie tylko "zablokowanego pliku" - nie działa
                self.files_list.selection_clear(0, tk.END)
                self.files_list.selection_set(index)
                print(f"Drag started: {self.dragged_item}")
            except Exception as e:
                print(f"Error starting drag: {e}")

    def on_drag_motion(self, event): # Obsługa dragu
        if self.dragged_item:
            # uwolnienie zaznaczenia
            self.files_list.selection_clear(0, tk.END)
            self.files_list.selection_set(self.dragged_item_index)

    def on_drop(self, event): # Obsługa dropu przenoszenie do drugiego okna
        self.drag_start_flag = False  # Reset drag flag
        if not self.dragged_item:
            return

        # Obsługa wyjątku dla tego samego okna lub braku przeciąganięcia na okno
        widget_under_cursor = self.winfo_containing(event.x_root, event.y_root)
        if isinstance(widget_under_cursor, tk.Listbox):
            destination_frame = widget_under_cursor.master
        else:
            print("Drop failed!")
            return

        if destination_frame is self.source_frame:
            print("Same Window!")
            return

        # Przenoszenie pliku
        try:
            source_path = os.path.join(self.source_frame.current_dir.get(), self.dragged_item)
            destination_path = os.path.join(destination_frame.current_dir.get(), self.dragged_item)
            #biblioteka shutil do przenoszenia plików
            shutil.move(source_path, destination_path)
            #odświeżenie layoutu
            self.source_frame.update_directory_contents(self.source_frame.current_dir.get())
            destination_frame.update_directory_contents(destination_frame.current_dir.get())
            #print(f"Moved {self.dragged_item} to {destination_path}")
        except Exception as e:
            print(f"Error during drop: {e}")

        # Czyszczenie atrybutów
        self.dragged_item = None
        self.dragged_item_index = None
        self.source_frame = None

    def on_item_double_click(self, event): # Nawigacja do folderu poprzez double-click
        self.drag_start_flag = False  # ustawienie flagi drag na false
        try:
            selection = self.files_list.get(self.files_list.curselection())
            current_path = self.current_dir.get()

            # Nawigacja do wybranego z listboxa folderu 
            new_path = os.path.join(current_path, selection)

            if os.path.isdir(new_path):  # obsługa kliknięcia na plik zamiast na folder
                self.update_directory_contents(new_path)
        except Exception as e:
            print(f"Error on double-click: {e}")

  