from tkinter import *


class Popup(Tk):
    def __init__(self):
        super().__init__()
        self.title("Message")
        self.geometry("300x150")
        self.focus()
