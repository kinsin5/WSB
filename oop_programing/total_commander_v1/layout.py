import tkinter as tk
from tkinter import ttk
from dpi import set_dpi_awareness

set_dpi_awareness()

list=[1,2,3,4,5,6]

root = tk.Tk()

list_tk = tk.StringVar(value=list)

root.geometry("600x400")
root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=3)
root.rowconfigure(0, weight=1)

frame1 = ttk.Frame(root, padding=(20,0,0,0))
frame1.grid(column=0, row=0, sticky="NSWE")
frame1.columnconfigure(0, weight=1)
frame1.rowconfigure(0, weight=1)
frame1.rowconfigure(1, weight=3)
frame1.rowconfigure(2, weight=1)

seperator = ttk.Separator(root, orient="vertical")
seperator.grid(column=1, row=0, sticky="NS")

frame2 = ttk.Frame(root, padding=(0,0,20,0))
frame2.grid(column=2, row=0,sticky="NSWE")
frame2.columnconfigure(0, weight=1)
frame2.rowconfigure(0, weight=1)
frame2.rowconfigure(1, weight=3)
frame2.rowconfigure(2, weight=1)

label1 = ttk.Label(frame1, text="label1")
label1.grid(column=0, row=0, sticky="NWE")

label2 = ttk.Label(frame2, text="label2")
label2.grid(column=0,row=0, sticky="NWE")


list1 = tk.Listbox(frame1, listvariable=list_tk)
list1.grid(column=0, row=1, sticky="NSWE")

list2 = tk.Listbox(frame2, listvariable=list_tk)
list2.grid(column=0, row=1,sticky="NSWE")

#N, E, S, W, NE, NW, SE, and SW

button1 = ttk.Button(frame1, text="button1")
button1.grid(column=0, row=2,sticky="")
button1 = ttk.Button(frame2, text="button2")
button1.grid(column=0, row=2,sticky="")


root.mainloop()