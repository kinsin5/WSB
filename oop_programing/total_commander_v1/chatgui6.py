import tkinter as tk
from tkinter import ttk
from dpi import set_dpi_awareness
import os
import time

set_dpi_awareness()

class SmallCommander(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Small Commander")
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=3)
        self.rowconfigure(0, weight=1)

        frame1 = Window_1(self)
        frame1.grid(row=0, column=0, sticky="NSEW")
      
        frame2 = Window_2(self)
        frame2.grid(row=0, column=2, sticky="NSEW")

        separator = ttk.Separator(orient="vertical")
        separator.grid(column=1, row=0, sticky="NS")

        # Bind keyboard shortcuts for F7 (create folder) and F8 (delete file)
        self.bind("<F7>", frame1.on_create_shortcut)  # F7 for create folder in Window 1
        self.bind("<F8>", frame1.on_delete_shortcut)  # F8 for delete in Window 1
        self.bind("<F5>", frame2.on_create_shortcut)  # F5 for create folder in Window 2
        self.bind("<F6>", frame2.on_delete_shortcut)  # F6 for delete in Window 2


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

        # Layout
        self.dir_label.grid(column=0, row=0, columnspan=2, sticky="N")
        self.parent_button.grid(column=0, row=1, sticky="EW")
        self.sort_name_button.grid(column=1, row=1, sticky="EW")
        self.sort_date_button.grid(column=2, row=1, sticky="EW")
        self.files_list.grid(column=0, row=2, sticky="NSWE")
        self.date_list.grid(column=1, row=2, columnspan=2, sticky="NSWE")
        self.delete_button.grid(column=0, row=3, sticky="")
        self.create_button.grid(column=1, row=3, columnspan=2, sticky="")

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # Populate the initial directory contents
        self.update_directory_contents(self.current_dir.get())

        # Bind double-click event
        self.files_list.bind("<Double-1>", self.on_item_double_click)

        # Bind drag-and-drop events
        self.files_list.bind("<ButtonPress-1>", self.start_drag)
        self.files_list.bind("<ButtonRelease-1>", self.complete_drag)
        self.files_list.bind("<B1-Motion>", self.drag_motion)

        # Initialize drag variables
        self.drag_data = {"item": None, "source": None}

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

    def start_drag(self, event):
        """Start the drag operation."""
        try:
            self.drag_data["item"] = self.files_list.get(self.files_list.nearest(event.y))
            self.drag_data["source"] = self
        except Exception as e:
            print(f"Error starting drag: {e}")

    def drag_motion(self, event):
        """Handle the motion during drag. (Optional for visual feedback.)"""
        # Placeholder for additional drag feedback if needed
        pass

    def complete_drag(self, event):
        """Complete the drag-and-drop operation."""
        try:
            target_widget = event.widget
            if isinstance(target_widget.master, (Window_1, Window_2)):  # Ensure the target is a valid window
                target_window = target_widget.master
                target_dir = target_window.current_dir.get()

                if self.drag_data["item"] and self.drag_data["source"]:
                    source_path = os.path.join(self.current_dir.get(), self.drag_data["item"])
                    target_path = os.path.join(target_dir, self.drag_data["item"])

                    if source_path != target_path:  # Avoid unnecessary operations
                        os.rename(source_path, target_path)

                        # Update both windows
                        self.update_directory_contents(self.current_dir.get())
                        target_window.update_directory_contents(target_dir)

                    # Reset drag data
                    self.drag_data = {"item": None, "source": None}
        except Exception as e:
            print(f"Error completing drag-and-drop: {e}")

    def go_to_parent(self):
        """Navigate to the parent directory."""
        current_path = self.current_dir.get()
        new_path = os.path.dirname(current_path)
        self.update_directory_contents(new_path)

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
        popup.geometry("200x100")
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





class Window_2(Window_1):  # Window_2 inherits all functionalities from Window_1
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.short1 = ttk.Label(self, text="[F6]")
        self.short2 = ttk.Label(self, text="[F5]")

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.short1.grid(column=0, row=4, sticky="N")
        self.short2.grid(column=1, row=4, columnspan=2, sticky="N")
        # Modify any specific behaviors for Window_2 here if needed
        # You can add additional buttons or change layout here if desired


if __name__ == "__main__":
    app = SmallCommander()
    app.geometry("900x600")

    app.mainloop()
