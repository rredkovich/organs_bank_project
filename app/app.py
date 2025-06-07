import tkinter as tk
from dataclasses import fields
from typing import List
from tkinter import ttk

from app.controllers.acceptor_controller import AcceptorController
from db import models


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Organs Bank")
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)

        acceptor_tab = ttk.Frame(notebook)
        notebook.add(acceptor_tab, text="Acceptors")
        AcceptorController(acceptor_tab)

    def run(self):
        self.root.mainloop()

# class App:
#     """Define the application class."""
#     def __init__(self, db_connection):
#         self.qs = QueryService(db_connection)
#         self.root = tk.Tk()
#         # self.label = tk.Label(self.root, text='hello world!', font='Arial 24')
#         # self.label.grid()
#
#     def run(self):
#         """Run the main loop."""
#         self.root.mainloop()


class Demo(App):
    def __init__(self, db_connection):
        super().__init__(db_connection)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)
        acceptor_tab = ttk.Frame(notebook)
        notebook.add(acceptor_tab, text="Acceptors")

        acceptors = self.qs.fetch_all(models.Acceptor)
        self.display_table(acceptors, parent=acceptor_tab, title="Acceptors", on_row_selected=self.on_row_selected)

    def on_row_selected(self, event):
        tree = event.widget  # This is the Treeview
        selected_item = tree.selection()
        if not selected_item:
            return

        item_id = selected_item[0]

        values = self.tree.item(item_id, "values")

        # Create a new top-level window
        top = tk.Toplevel(self.root)
        top.title(f"Details for Acceptor {values[0]}")
        for i, value in enumerate(values):
            label = ttk.Label(top, text=f"{self.tree['columns'][i]}: {value}")
            label.pack(anchor='w', padx=10, pady=5)

    def display_table(self, entities: List["BaseDT"], parent=None,  title="", on_row_selected=None):
        if not parent:
            parent = self.root
        self.main_title = tk.Label(parent, text='Display a 2D table', font='Arial 24')
        self.title = tk.Label(parent, text='Click on header to sort')
        self.main_title.grid(row=0, column=0)
        self.title.grid(row=1, column=0)

        tree = ttk.Treeview(parent)
        self.tree = tree
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=3, column=1, sticky='ns')
        tree.grid(row=3, column=0)
        cols = tuple(f.name for f in fields(entities[0]))
        for entity in entities:
            values = tuple(getattr(entity, col) for col in cols)
            tree.insert('','end', values=values)

        tree['columns'] = cols
        def cal_width(col_name, col_value):
            widest = max((col_name, col_value, ), key=lambda x: len(str(x)))
            return round(len(str(widest)) * 10 + len(str(widest)) * 0.45)

        for i, col in enumerate(cols):
            tree.column(i, width=cal_width(col, values[i]), anchor='e')
            tree.heading(i, text=col)

        if on_row_selected:
            tree.bind("<Double-1>", self.on_row_selected)