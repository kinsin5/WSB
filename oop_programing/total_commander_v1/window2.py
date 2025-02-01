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
        self.dragged_item = None  # To store the dragged item
        self.source_frame = None  # To track the source frame during drag
        self.drag_start_flag = False  # Flag to track if a drag is starting
        
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
            child.grid_configure(padx=8, pady=8)
        self.files_list.grid_configure(padx=0)
        self.date_list.grid_configure(padx=0)
        
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
        
        self.files_list.bind("<ButtonPress-1>", self.on_drag_start)
        self.files_list.bind("<B1-Motion>", self.on_drag_motion)
        self.files_list.bind("<ButtonRelease-1>", self.on_drop)

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
        popup.geometry(f"{window_width}x{window_height - 100}+{x}+{y}")

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

    def on_drag_start(self, event):
        """Handle the start of a drag event."""
        self.drag_start_flag = True  # Set the drag flag
        self.after(200, self._start_drag, event)  # Add a small delay

    def _start_drag(self, event):
        """Start the drag after a delay, if the flag is still set."""
        if self.drag_start_flag:
            try:
                index = self.files_list.nearest(event.y)  # Lock the file at the start
                self.files_list.selection_clear(0, tk.END)  # Clear any accidental selection changes
                self.files_list.selection_set(index)  # Ensure the correct file is selected
                self.dragged_item = self.files_list.get(index)
                self.source_frame = self
                print(f"Drag started: {self.dragged_item}")
            except Exception as e:
                print(f"Error starting drag: {e}")

    def on_drag_motion(self, event):
        """Handle the motion of a drag event."""
        if self.dragged_item:
            # Optional: Visual feedback during drag
            pass

    def on_drop(self, event):
        """Handle the drop event."""
        self.drag_start_flag = False  # Reset the drag flag
        if not self.dragged_item:
            return

        # Determine the destination frame
        widget_under_cursor = self.winfo_containing(event.x_root, event.y_root)
        if isinstance(widget_under_cursor, tk.Listbox):
            destination_frame = widget_under_cursor.master
        else:
            print("Drop failed: No valid destination frame.")
            return

        if destination_frame is self.source_frame:
            print("Item dropped on the same frame; no action taken.")
            return

        # Move the file
        try:
            source_path = os.path.join(self.source_frame.current_dir.get(), self.dragged_item)
            destination_path = os.path.join(destination_frame.current_dir.get(), self.dragged_item)

            shutil.move(source_path, destination_path)

            self.source_frame.update_directory_contents(self.source_frame.current_dir.get())
            destination_frame.update_directory_contents(destination_frame.current_dir.get())
            print(f"Moved {self.dragged_item} to {destination_path}")
        except Exception as e:
            print(f"Error during drop: {e}")

        self.dragged_item = None
        self.source_frame = None

    def on_item_double_click(self, event):
        """Handle double-clicking on an item in the listbox."""
        self.drag_start_flag = False  # Cancel any drag operation
        try:
            selection = self.files_list.get(self.files_list.curselection())
            current_path = self.current_dir.get()

            # Navigate into the selected folder
            new_path = os.path.join(current_path, selection)

            if os.path.isdir(new_path):  # Only navigate if it's a directory
                self.update_directory_contents(new_path)
        except Exception as e:
            print(f"Error on double-click: {e}")

    