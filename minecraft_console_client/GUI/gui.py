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
        self.protocol("WM_DELETE_WINDOW", self.close)
        print("Created GUI")

    def set_value(self, target: str, value):
        """ Display 'target: value' """
        if target in self.data:
            self.data[target]['text'] = f"{target}: {value}"
        else:
            self.data[target] = tk.Label(master=self,
                                         text=f"{target}: {value}",
                                         width=50,
                                         anchor="w")
            self.data[target].grid()

        self.update()

    def do_nothing(self, *args):
        """ Does nothing """
        pass

    def close(self):
        """ Closes tkinter window, and changes set_value() to do_nothing() """
        import types
        self.set_value = types.MethodType(self.do_nothing, self)
        self.destroy()
        print("Closed GUI")

    def keep_alive(self):
        """ Keeps window not frozen. """
        self.after(1000, self.keep_alive)
        self.update()

