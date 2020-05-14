import tkinter as tk
from tkinter import Frame


class GUI(tk.Tk):
    position_frame: Frame = None
    data: dict = {
       # "x": tk.Label(),
    }

    def __init__(self):
        super(GUI, self).__init__()
        self.grid()
        self.keep_alive()
        print("Created GUI")

    def set_value(self, target: str, value):
        """ Display 'target: value' """
        if target in self.data:
            self.data[target]['text'] = f"{target}: {value}"
        else:
            self.data[target] = tk.Label(master=self,
                                         text=f"{target}: {value}",
                                         width=50)
            self.data[target].grid()

        self.update()

    def keep_alive(self):
        self.after(1000, self.keep_alive)
        self.update()

