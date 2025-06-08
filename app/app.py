import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from app.controllers.acceptor_controller import AcceptorController
from app.controllers.donor_controller import DonorController

from db.export_import import DBExporterImporter


class App:
    def __init__(self):
        self.initialize()
        self.create_menu()

    def initialize(self):
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
        file_menu.add_separator()
        file_menu.add_command(label="Export Database...", command=self.export_database)
        file_menu.add_command(label="Import Database...", command=self.import_database)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

    def export_database(self):
        path = filedialog.askdirectory(
            mustexist=False,
            title="Export Database Files To..."
        )
        if path:
            dbex = DBExporterImporter()
            try:
                dbex.export_all(path)
                messagebox.showinfo("Success", f"Database exported")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed:\n{str(e)}")

    def import_database(self):
        path = filedialog.askdirectory(
            mustexist=False,
            title="Export Database Files To..."
        )
        if path:
            dbex = DBExporterImporter()
            try:
                dbex.import_all(path)
                messagebox.showinfo("Success", f"Database imported")
                self.initialize()
            except Exception as e:
                messagebox.showerror("Error", f"Import failed:\n{str(e)}")



    def run(self):
        self.root.mainloop()
