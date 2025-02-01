import tkinter as tk
from tkinter import ttk
from dpi import set_dpi_awareness
import os

set_dpi_awareness()

class SmallCommander(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = "Small Commander"
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=3)
        self.rowconfigure(0, weight=1)


        frame1 = Window_1(self)
        frame1.grid(row=0, column=0, sticky="NSEW")
      
        frame2 = Window_2(self)
        frame2.grid(row=0, column=2, sticky="NSEW")

        seperator = ttk.Separator(orient="vertical")
        seperator.grid(column=1, row=0, sticky="NS")


class Window_1(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.current_dir = tk.StringVar(value=os.getcwd())  # Start with the current working directory
        self.list_value = tk.StringVar(value=[])

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)
        self.rowconfigure(2, weight=1)
        # UI Components
        self.dir_label = ttk.Label(self, textvariable=self.current_dir)
        self.files_list = tk.Listbox(self, listvariable=self.list_value)
        self.button = ttk.Button(self, text="Remove")  # Example button

        # Layout
        self.dir_label.grid(column=0, row=0, sticky="")
        self.button.grid(column=0, row=2, sticky="")
        self.files_list.grid(column=0, row=1, sticky="NSWE")

        for child in self.winfo_children():
            child.grid_configure(padx=15, pady=15)

        # Populate the initial directory contents
        self.update_directory_contents(self.current_dir.get())

        # Bind double-click event
        self.files_list.bind("<Double-1>", self.on_item_double_click)

    def update_directory_contents(self, path):
        """Update the listbox to show the contents of the directory."""
        try:
            items = os.listdir(path)
            # Add '..' to represent the parent directory
            items = [".."] + items
            self.list_value.set(items)
            self.current_dir.set(path)
        except Exception as e:
            print(f"Error loading directory {path}: {e}")

    def on_item_double_click(self, event):
        """Handle double-clicking on an item in the listbox."""
        selection = self.files_list.get(self.files_list.curselection())
        current_path = self.current_dir.get()

        if selection == "..":
            # Navigate to the parent directory
            new_path = os.path.dirname(current_path)
        else:
            # Navigate into the selected folder
            new_path = os.path.join(current_path, selection)
        
        if os.path.isdir(new_path):  # Only navigate if it's a directory
            self.update_directory_contents(new_path)


class Window_2(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.current_dir = tk.StringVar(value=os.getcwd())  # Start with the current working directory
        self.list_value = tk.StringVar(value=[])
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)
        self.rowconfigure(2, weight=1)
        # UI Components
        self.dir_label = ttk.Label(self, textvariable=self.current_dir)
        self.files_list = tk.Listbox(self, listvariable=self.list_value)
        self.button = ttk.Button(self, text="Make dir")  # Example button

        # Layout
        self.dir_label.grid(column=0, row=0, sticky="")
        self.button.grid(column=0, row=2, sticky="")
        self.files_list.grid(column=0, row=1, sticky="NSWE")

        for child in self.winfo_children():
            child.grid_configure(padx=15, pady=15)

        # Populate the initial directory contents
        self.update_directory_contents(self.current_dir.get())

        # Bind double-click event
        self.files_list.bind("<Double-1>", self.on_item_double_click)

    def update_directory_contents(self, path):
        """Update the listbox to show the contents of the directory."""
        try:
            items = os.listdir(path)
            # Add '..' to represent the parent directory
            items = [".."] + items
            self.list_value.set(items)
            self.current_dir.set(path)
        except Exception as e:
            print(f"Error loading directory {path}: {e}")

    def on_item_double_click(self, event):
        """Handle double-clicking on an item in the listbox."""
        selection = self.files_list.get(self.files_list.curselection())
        current_path = self.current_dir.get()

        if selection == "..":
            # Navigate to the parent directory
            new_path = os.path.dirname(current_path)
        else:
            # Navigate into the selected folder
            new_path = os.path.join(current_path, selection)
        
        if os.path.isdir(new_path):  # Only navigate if it's a directory
            self.update_directory_contents(new_path)



if __name__ == "__main__":
    app = SmallCommander()
    app.geometry("900x600")

    app.mainloop()