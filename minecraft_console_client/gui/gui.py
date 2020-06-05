from typing import Any

import tkinter as tk

gui = None


class GUI(tk.Tk):
    position_frame: tk.Frame = None
    data: dict = {
        # "x": tk.Label(),
    }

    def __init__(self):
        super(GUI, self).__init__()
        self.grid()
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.hotbar_messages = []
        self.chat_messages = []

        self.data_frame = tk.Frame(self)
        self.messages_frame = tk.Frame(self)

        self.data_frame.grid(row=0, column=0, sticky="nw")
        self.messages_frame.grid(row=0, column=1, sticky="nw")

        self.hotbar_frame = tk.LabelFrame(self.messages_frame,
                                          text="HOTBAR",
                                          labelanchor="n")
        self.chat_frame = tk.LabelFrame(self.messages_frame,
                                        text="CHAT",
                                        labelanchor="n")

        self.hotbar_frame.grid(row=0, column=0, sticky="nw")
        self.chat_frame.grid(row=1, column=0, sticky="nw")

        self.hotbar = tk.Label(self.hotbar_frame, anchor="nw")
        self.chat = tk.Label(self.chat_frame, anchor="nw")

        self.hotbar.grid()
        self.chat.grid()

        print("Created gui")
        self.keep_alive()

    # TODO: optimize
    def add_to_chat(self, message):
        self.chat_messages.append(message)
        if len(self.chat_messages) > 20:
            self.chat_messages.pop(0)
        self.chat['text'] = '\n'.join(self.chat_messages)

        self.update()

    def add_to_hotbar(self, message):
        self.hotbar_messages.append(message)
        if len(self.hotbar_messages) > 20:
            self.hotbar_messages.pop(0)
        self.hotbar['text'] = '\n'.join(self.hotbar_messages)

        self.update()

    def set_labels(self, *labels: (str, Any)):
        """
        Display 'name: value' for pair in labels.

        :param labels: tuple of pairs
        """
        for label in labels:
            name = label[0]
            value = label[1]
            if name in self.data:
                self.data[name]['text'] = f"{name}: {value}"
            else:
                self.data[name] = tk.Label(master=self.data_frame,
                                           text=f"{name}: {value}",
                                           width=50,
                                           anchor="w")
                self.data[name].grid(column=0)

        self.update()

    def do_nothing(self, *args):
        """ Does nothing """
        pass

    def close(self):
        """ Closes tkinter window, and changes set_labels(() to do_nothing() """
        import types
        self.set_labels = types.MethodType(self.do_nothing, self)
        self.destroy()
        print("Closed gui")

    def keep_alive(self):
        """ Keeps window not frozen. """
        # self.update_idletasks()
        # self.update()
        # self.after(100, self.keep_alive)

