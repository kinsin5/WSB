import tkinter as tk
from tkinter import ttk
from dpi import set_dpi_awareness
import os

set_dpi_awareness()

class SmallCommander(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = "Small Commander"


        frame1 = Window_1(self)
        frame1.grid(row=0, column=0, sticky="NSEW")
        frame1.columnconfigure(0, weight=1)
        frame1.rowconfigure(0, weight=1)
        frame1.rowconfigure(1, weight=5)
        frame1.rowconfigure(2, weight=1)

        frame2 = Window_2(self)
        frame2.grid(row=0, column=2, sticky="NSEW")
        frame2.columnconfigure(0, weight=1)
        frame2.rowconfigure(0, weight=1)
        frame2.rowconfigure(1, weight=5)
        frame2.rowconfigure(2, weight=1)

        seperator = ttk.Separator(self, orient="vertical")
        seperator.grid(column=1, row=0, sticky="NS")


class Window_1(ttk.Frame):
    def __init__(self, container, **kwargs):
          super().__init__(container, **kwargs)

          self.current_dir = tk.StringVar(value="string string path")
          self.list_value = tk.StringVar(value=[1,2,3,4,5])
          
          dir_label = ttk.Label(self, textvariable=self.current_dir)
          files_list = tk.Listbox(self, listvariable=self.list_value)
          button = ttk.Button(self, text="Remove")
          

          dir_label.grid(column=0, row=0, sticky="NWE")
          button.grid(column=0, row=2,sticky="")
          files_list.grid(column=0, row=1, sticky="NSWE")

          for child in self.winfo_children():
             child.grid_configure(padx=15, pady=15)

          #set_os_vars(self)

    # #def set_os_vars(self, *args):
    #     try:
    #          file_list = os.listdir()
    #          self.list_value.set(value=file_list)
    #          curr_dir = os.getcwd()
    #          self.list_value.set(curr_dir)
    #     except ValueError:
    #          pass
    

         

class Window_2(Window_1):
     def __init__(self, container, **kwargs):
          super().__init__(container, **kwargs)

         
          button = ttk.Button(self, text="Make Folder")
          button.grid(column=0, row=2,sticky="")

         
root = SmallCommander()

root.geometry("600x400")
root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=3)
root.rowconfigure(0, weight=1)

root.mainloop()

print(os.listdir())
print(os.getcwd())
          
class Meters_to_Feet(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)
        
        self.meters_value = tk.StringVar()
        self.feet_value = tk.StringVar()

        meter_label = ttk.Label(self, text="Meters:")
        meter_entry = ttk.Entry(self, textvariable=self.meters_value)

        feet_label = ttk.Label(self, text="Feet:")
        feet_calc = ttk.Label(self, textvariable=self.feet_value)

        calculate_butt = ttk.Button(self, text="Calculate", command=self.calculate)
        meter_label.grid(column=0, row=0, sticky="W")
        meter_entry.grid(column=1, row=0, sticky="EW")
        feet_label.grid(column=0, row=1, sticky="W")
        feet_calc.grid(column=1, row=1, sticky="EW")
        calculate_butt.grid(column=0, row=2, columnspan=2, sticky="EW")
    
        for child in self.winfo_children():
             child.grid_configure(padx=15, pady=15)
    

    def calculate(self, *args):
        try:
                m = float(self.meters_value.get())
                feet = m * 3.28084
                self.feet_value.set(f"{feet:.3f}")
        except ValueError:
            pass

class Feet_to_Meters(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)
        
        self.meters_value = tk.StringVar()
        self.feet_value = tk.StringVar()

        feet_label = ttk.Label(self, text="Feet:")
        feet_entry = ttk.Entry(self, textvariable=self.feet_value)

        meter_label = ttk.Label(self, text="Meter:")
        meter_calc = ttk.Label(self, textvariable=self.meters_value)

        calculate_butt = ttk.Button(self, text="Calculate", command=self.calculate)
        feet_label.grid(column=0, row=0, sticky="W")
        feet_entry.grid(column=1, row=0, sticky="EW")
        meter_label.grid(column=0, row=1, sticky="W")
        meter_calc.grid(column=1, row=1, sticky="EW")
        calculate_butt.grid(column=0, row=2, columnspan=2, sticky="EW")
    
        for child in self.winfo_children():
             child.grid_configure(padx=15, pady=15)
    

    def calculate(self, *args):
        try:
                feet = float(self.feet_value.get())
                m = feet / 3.28084
                self.meters_value.set(f"{m:.3f}")
        except ValueError:
            pass


