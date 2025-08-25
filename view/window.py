import tkinter as tk

class Window():
    def __init__(self, config = None):
        self.window = tk.Tk()
        if config:
            self.window.title(config.title)
    def setup(self, config = None):
        if config == None:
            return
        
        # Configure the window

    