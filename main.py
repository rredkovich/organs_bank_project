import sqlite3
import tkinter as tk
from tkinter import ttk
from db import initialise_db
from db.query_service import QueryService
from db import models
from dataclasses import fields

db_name = 'dev.db'

conn = sqlite3.connect(db_name)

# initialise_db.create_tables(conn)
# initialise_db.prefill_lib_data(conn)




class App:
    """Define the application class."""
    def __init__(self):
        self.qs = QueryService(conn)
        self.root = tk.Tk()
        # self.label = tk.Label(self.root, text='hello world!', font='Arial 24')
        # self.label.grid()

    def run(self):
        """Run the main loop."""
        self.root.mainloop()


class Demo(App):
    def __init__(self):
        super().__init__()
        self.main_title = tk.Label(self.root, text='Display a 2D table', font='Arial 24')
        self.title = tk.Label(self.root, text='Click on header to sort')
        self.main_title.grid(row=0, column=0)
        self.title.grid(row=1, column=0)
        acceptors = self.qs.fetch_all(models.Acceptor)

        tree = ttk.Treeview(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=3, column=1, sticky='ns')
        tree.grid(row=3, column=0)
        cols = tuple(f.name for f in fields(acceptors[0]))
        for acceptor in acceptors:
            values = tuple(getattr(acceptor, col) for col in cols)
            tree.insert('','end', values=values)

        tree['columns'] = cols
        def cal_width(col_name, col_value):
            widest = max((col_name, col_value, ), key=lambda x: len(str(x)))
            return round(len(str(widest)) * 10 + len(str(widest)) * 0.45)

        for i, col in enumerate(cols):
            tree.column(i, width=cal_width(col, values[i]), anchor='e')
            tree.heading(i, text=col)


if __name__ == '__main__':
    app = Demo()
    app.run()