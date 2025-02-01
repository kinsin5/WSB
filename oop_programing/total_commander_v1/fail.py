import tkinter as tk
from tkinter import ttk
from dpi import set_dpi_awareness
import os
from datetime import datetime

set_dpi_awareness()

class SmallCommander(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        self.title("Small Commander")
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=3)
        self.rowconfigure(0, weight=1)

        frame1 = Window(self)
        frame1.grid(row=0, column=0, sticky="NSEW")

        frame2 = Window(self)
        frame2.grid(row=0, column=2, sticky="NSEW")

        separator = ttk.Separator(orient="vertical")
        separator.grid(row=0, column=1, sticky="NS")


class Window(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.current_dir = tk.StringVar(value=os.getcwd())  # Start with the current working directory
        self.list_items = []  # Stores tuples of (name, date) for display
        self.sort_criterion = "name"  # Default sort criterion

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=5)
        self.rowconfigure(3, weight=1)

        # UI Components
        self.dir_label = ttk.Label(self, textvariable=self.current_dir)
        self.parent_button = ttk.Button(self, text="Parent Folder", command=self.go_to_parent)
        self.sort_name_button = ttk.Button(self, text="Sort by Name", command=lambda: self.update_directory_contents(self.current_dir.get(), "name"))
        self.sort_date_button = ttk.Button(self, text="Sort by Date", command=lambda: self.update_directory_contents(self.current_dir.get(), "date"))

        # Frame for lists
        self.list_frame = ttk.Frame(self)
        self.list_frame.columnconfigure(0, weight=1)
        self.list_frame.columnconfigure(1, weight=1)
        self.list_frame.rowconfigure(0, weight=1)

        # Listboxes for file names and dates
        self.files_list = tk.Listbox(self.list_frame, selectmode=tk.SINGLE)
        self.dates_list = tk.Listbox(self.list_frame, selectmode=tk.SINGLE)
        # Synchronize scrolling
        self.files_list.bind("<<ListboxSelect>>", self.sync_selection)
        self.files_list.bind("<<ListboxSelect>>", self.sync_selection)
        self.files_list.bind("<MouseWheel>", self.sync_scroll)
        self.dates_list.bind("<MouseWheel>", self.sync_scroll)

        self.files_list.bind("<Double-1>", self.on_item_double_click)

        self.button = ttk.Button(self, text="Make dir")  # Example button

        # Layout
        self.dir_label.grid(column=0, row=0, sticky="W", padx=5, pady=5)
        self.parent_button.grid(column=0, row=1, sticky="W", padx=5, pady=5)
        self.sort_name_button.grid(column=0, row=1, sticky="E", padx=5, pady=5)
        self.sort_date_button.grid(column=0, row=1, sticky="E", padx=(5, 90), pady=5)
        self.list_frame.grid(column=0, row=2, sticky="NSWE", padx=5, pady=5)
        self.files_list.grid(column=0, row=0, sticky="NSWE")
        self.dates_list.grid(column=1, row=0, sticky="NSWE")
        self.button.grid(column=0, row=3, sticky="W", padx=5, pady=5)

        # Populate the initial directory contents
        self.update_directory_contents(self.current_dir.get(), self.sort_criterion)

    def sync_selection(self, event):
        """Synchronize selection between the two lists."""
        selected_index = event.widget.curselection()
        if selected_index:
            self.files_list.select_set(selected_index)
            self.dates_list.select_set(selected_index)
        else:
            self.files_list.selection_clear(0, tk.END)
            self.dates_list.selection_clear(0, tk.END)

    def sync_scroll(self, event):
         """Synchronize scrolling between the two lists."""
         self.files_list.yview_scroll(-1 * (event.delta // 120), "units")
         self.dates_list.yview_scroll(-1 * (event.delta // 120), "units")

    def update_directory_contents(self, path, sort_by):
        """Update the listbox to show the contents of the directory."""
        try:
            items = os.listdir(path)
            self.list_items = []

            for item in items:
                item_path = os.path.join(path, item)
                creation_date = datetime.fromtimestamp(os.path.getctime(item_path)).strftime('%Y-%m-%d %H:%M:%S')
                self.list_items.append((item, creation_date))

            # Sort items based on the criterion
            if sort_by == "name":
                self.list_items = sorted(self.list_items, key=lambda x: x[0].lower())
            elif sort_by == "date":
                self.list_items = sorted(self.list_items, key=lambda x: x[1])

            # Update Listboxes
            self.files_list.delete(0, tk.END)
            self.dates_list.delete(0, tk.END)
            for name, date in self.list_items:
                self.files_list.insert(tk.END, name)
                self.dates_list.insert(tk.END, date)

            self.current_dir.set(path)
            self.sort_criterion = sort_by
        except Exception as e:
            print(f"Error loading directory {path}: {e}")

    def on_item_double_click(self, event):
        selection = self.files_list.get(self.files_list.curselection())
        current_path = self.current_dir.get()
        new_path = os.path.join(current_path, selection)
        if os.path.isdir(new_path):  # Only navigate if it's a directory
            self.update_directory_contents(new_path, self.sort_criterion)
    def on_item_double_click(self, event):
        """Handle double-clicking on an item in the listbox."""
        try:
            selection_index = self.files_list.curselection()
            if not selection_index:
                return
            selection = self.files_list.get(selection_index[0])
            current_path = self.current_dir.get()

            new_path = os.path.join(current_path, selection)
            if os.path.isdir(new_path):
                self.update_directory_contents(new_path, self.sort_criterion)
        except Exception as e:
            print(f"Error navigating to folder: {e}")

    def go_to_parent(self):
        """Navigate to the parent directory."""
        current_path = self.current_dir.get()
        new_path = os.path.dirname(current_path)
        self.update_directory_contents(new_path, self.sort_criterion)

if __name__ == "__main__":
    app = SmallCommander()
    app.geometry("900x600")

    app.mainloop()