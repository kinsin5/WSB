import tkinter as tk
from tkinter import ttk
import os
import time
import shutil

class Window_1(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.current_dir = tk.StringVar(value=os.getcwd())  # Start with the current working directory
        self.list_value = tk.StringVar(value=[])
        self.date_value = tk.StringVar(value=[])

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=10)
        self.rowconfigure(3, weight=2)

        # UI Components
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
        

        # Layout
        self.dir_label.grid(column=0, row=0, columnspan=2, sticky="N")
        self.parent_button.grid(column=0, row=1, sticky="EW")
        self.sort_name_button.grid(column=1, row=1, sticky="EW")
        self.sort_date_button.grid(column=2, row=1, sticky="EW")
        

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.delete_button.grid(column=0, row=3, sticky="")
        self.create_button.grid(column=1, row=3, columnspan=2, sticky="")
        self.files_list.grid(column=0, row=2, sticky="NSWE")
        self.date_list.grid(column=1, row=2, columnspan=2, sticky="NSWE")
        self.short1.grid(column=0, row=4, sticky="N")
        self.short2.grid(column=1, row=4, columnspan=2, sticky="N")

        # Populate the initial directory contents
        self.update_directory_contents(self.current_dir.get())

        # Bind double-click event
        self.files_list.bind("<Double-1>", self.on_item_double_click)

        # Track the selected item in the listbox
        self.selected_item = None
        self.files_list.bind("<<ListboxSelect>>", self.on_listbox_select)

    def update_directory_contents(self, path):
        """Update the listbox to show the contents of the directory."""
        try:
            items = os.listdir(path)
            items = [os.path.abspath(path)] + items if path != os.path.abspath(path) else items
            self.list_value.set(items)
            self.date_value.set([time.ctime(os.path.getctime(os.path.join(path, item))) for item in items])
            self.current_dir.set(path)
        except Exception as e:
            print(f"Error loading directory {path}: {e}")

    def go_to_parent(self):
        """Navigate to the parent directory."""
        current_path = self.current_dir.get()
        new_path = os.path.dirname(current_path)
        self.update_directory_contents(new_path)

    def on_item_double_click(self):
        """Handle double-clicking on an item in the listbox."""
        selection = self.files_list.get(self.files_list.curselection())
        current_path = self.current_dir.get()

        # Navigate into the selected folder
        new_path = os.path.join(current_path, selection)

        if os.path.isdir(new_path):  # Only navigate if it's a directory
            self.update_directory_contents(new_path)

    def sort_by_name(self):
        """Sort the file list by name (A to Z) - case insensitive."""
        current_path = self.current_dir.get()
        items = os.listdir(current_path)
        items.sort(key=lambda item: item.lower())  # Sorting by lowercase version of the item name
        self.list_value.set(items)
        self.date_value.set([time.ctime(os.path.getctime(os.path.join(current_path, item))) for item in items])

    def sort_by_date(self):
        """Sort the file list by creation date."""
        current_path = self.current_dir.get()
        items = os.listdir(current_path)
        items.sort(key=lambda item: os.path.getctime(os.path.join(current_path, item)))
        self.list_value.set(items)
        self.date_value.set([time.ctime(os.path.getctime(os.path.join(current_path, item))) for item in items])

    def delete_item(self):
        """Delete selected item (file or folder)."""
        if self.selected_item is None:
            print("No item selected")
            return

        current_path = self.current_dir.get()
        path_to_delete = os.path.join(current_path, self.selected_item)

        try:
            if os.path.isdir(path_to_delete):
                os.rmdir(path_to_delete)
            else:
                os.remove(path_to_delete)
            self.update_directory_contents(current_path)
        except Exception as e:
            print(f"Error deleting {path_to_delete}: {e}")

    def create_folder(self):
        """Create a new folder in the current directory."""
        current_path = self.current_dir.get()

        # Popup to enter folder name
        popup = tk.Toplevel(self)
        popup.title("Create New Folder")
        # Center the popup window
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        window_width = popup.winfo_reqwidth()
        window_height = popup.winfo_reqheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        popup.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Entry widget for folder name
        folder_name_entry = tk.Entry(popup)
        folder_name_entry.pack(padx=10, pady=10)

        # Button to confirm folder creation
        def confirm_create():
            folder_name = folder_name_entry.get()
            if folder_name:
                folder_path = os.path.join(current_path, folder_name)
                try:
                    os.mkdir(folder_path)
                    self.update_directory_contents(current_path)
                    popup.destroy()  # Close popup after folder is created
                except Exception as e:
                    print(f"Error creating folder {folder_path}: {e}")
            else:
                print("Folder name cannot be empty")

        confirm_button = tk.Button(popup, text="Create", command=confirm_create)
        confirm_button.pack(padx=10, pady=10)

    def on_delete_shortcut(self, event):
        """Handle F8 keyboard shortcut for deletion."""
        self.delete_item()

    def on_create_shortcut(self, event):
        """Handle F7 keyboard shortcut for folder creation."""
        self.create_folder()

    def on_listbox_select(self, event):
        """Update the selected item when the user selects an item in the listbox."""
        selection = self.files_list.get(self.files_list.curselection())
        self.selected_item = selection
        print(f"Selected item: {self.selected_item}")