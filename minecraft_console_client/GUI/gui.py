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

        self.data_frame = Frame(self)
        self.data_frame.grid(row=0, column=0, sticky="nw")

        self.chat_frame = Frame(self)
        self.chat_frame.grid(row=0, column=1, sticky="nw")
        self.chat_messages = []

        self.chat = tk.Label(self.chat_frame, anchor="nw")
        self.chat.grid()

        print("Created GUI")

    # TODO: optimize
    def add_to_chat(self, message):
        self.chat_messages.append(message)
        if len(self.chat_messages) > 20:
            self.chat_messages.pop(0)
        self.chat['text'] = '\n'.join(self.chat_messages)

        self.update()

    def set_value(self, target: str, value):
        """ Display 'target: value' """
        if target in self.data:
            self.data[target]['text'] = f"{target}: {value}"
        else:
            self.data[target] = tk.Label(master=self.data_frame,
                                         text=f"{target}: {value}",
                                         width=50,
                                         anchor="w")
            self.data[target].grid(column=0)

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

