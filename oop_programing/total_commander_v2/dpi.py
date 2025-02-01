##just a quick import to help my dpi in app.

def set_dpi_awareness():
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass