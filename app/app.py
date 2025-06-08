import tkinter as tk
from tkinter import ttk, messagebox

from app.controllers.acceptor_controller import AcceptorController
from app.controllers.donor_controller import DonorController


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Organs Bank")
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)

        acceptor_tab = ttk.Frame(notebook)
        notebook.add(acceptor_tab, text="Acceptors")
        self.acceptor_controller = AcceptorController(acceptor_tab)

        donors_tab = ttk.Frame(notebook)
        notebook.add(donors_tab, text="Donors")
        self.donor_controller = DonorController(donors_tab)

        self.create_menu()

    def create_menu(self):
        def about():
            messagebox.showinfo("About", '\n'.join(("Organs bank project",
                                                   "Created by Roman Redkovich",
                                                   "08.06.2025")))

        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New Donor", command=self.donor_controller.create_new)
        file_menu.add_command(label="New Acceptor", command=self.acceptor_controller.create_new)
        menu_bar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

    def run(self):
        self.root.mainloop()
