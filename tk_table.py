"""Display a 2D table."""

#
import tkinter as tk
from tkinter import ttk
import random

class App:
    """Define the application class."""
    def __init__(self):

        self.root = tk.Tk()
        # self.label = tk.Label(self.root, text='hello world!', font='Arial 24')
        # self.label.grid()

    def run(self):
        """Run the main loop."""
        self.root.mainloop()

n, m = 40, 10
table = []
for i in range(n):
    line = []
    for j in range(m):
        line.append(random.randint(0, 999))
    table.append(line)

class EntryMixin:
    """Add label, widget and callback function."""

    # def add_widget(self, label, widget, kwargs):
    #     """Add widget with optional label."""
    #     if label == '':
    #         super(widget, self).__init__(App.stack[-1], **kwargs)
    #         self.grid()
    #     else:
    #         d = 2 if App.debug else 0
    #         frame = ttk.Frame(App.stack[-1], relief='solid', borderwidth=d)
    #         frame.grid(sticky='e')
    #         ttk.Label(frame, text=label).grid()
    #         super(widget, self).__init__(frame, **kwargs)
    #         self.grid(row=0, column=1)

    def add_cmd(self, cmd):
        # if cmd is a string store it, and replace it 'cb' callback function
        # if isinstance(cmd, str):
        #     self.cmd = cmd
        #     cmd = self.cb
        self.bind('<Return>', lambda event: cmd(self, event))

    def cb(self, item=None, event=None):
        """Execute the cmd string in the widget context."""
        exec(self.cmd)


class Combobox(ttk.Combobox, EntryMixin):
    """Create a Combobox with callback."""

    def __init__(self, master, values='', cmd='', **kwargs):
        kwargs.update({'values': values})
        super().__init__(master, **kwargs)
        if isinstance(values, str):
            values = values.split(';')

        self.var = tk.StringVar()
        # self.var.set(values[val])

        # self.add_widget(label, Combobox, kwargs)
        # self['textvariable'] = self.var

        # self.add_cmd(cmd)
        # self.bind('<<ComboboxSelected>>', self.cb)

def prt(*args, **kwargs):
    for arg in args:
        print(arg)

    for k, v in kwargs.items():
        print(k, v)

class Demo(App):
    def __init__(self):
        super().__init__()
        self.main_title = tk.Label(self.root, text='Display a 2D table', font='Arial 24')
        self.title = tk.Label(self.root, text='Click on header to sort')
        self.main_title.grid(row=0, column=0)
        self.title.grid(row=1, column=0)

        # choice = tk.StringVar()
        # days = 'Monday', 'Tuesday', 'Friday', 'Saturday', 'Sunday'
        # combo=Combobox(master=self.root, values=days, textvariable=choice)#.grid(row=2, column=0)
        # combo.add_cmd(prt)
        # combo.grid(row=2, column=0)



        tree = ttk.Treeview(self.root)
        tree.grid()
        for i in range(n):
            tree.insert('','end', text=table[i][0], values=table[i][1:])
        #
        tree['columns'] = list(range(m-1))
        headings=list('ABCDEFGHI')
        for j in range(m-1):
            tree.column(j, width=50, anchor='e')
            tree.heading(j, text=headings[j])


# App().run()
Demo().run()