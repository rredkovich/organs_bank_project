import io, datetime
import tkinter as tk
from tkinter import ttk
from typing import List, Any


class BaseAppListView(ttk.Frame):
    def __init__(self, parent, controller, columns: List[str], double_click_callback=None):
        super().__init__(master=parent)
        self.double_click_callback = double_click_callback
        self.controller = controller
        # headings?
        #self.tree = ttk.Treeview(master=self, headinds=columns, show="headings")
        self.tree = ttk.Treeview(master=parent, show="headings")

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=3, column=1, sticky='ns')
        self.tree.grid(row=3, column=0)

        self.tree['columns'] = columns
        for i, col in enumerate(columns):
            self.tree.column(i, width=self._cal_width(col, 0), anchor='e')
            self.tree.heading(i, text=col)

        # self.tree.pack(fill='both', expand=True)
        self.tree.bind('<Double-1>', self._on_double_click)

    def _cal_width(self, col_name, col_value):
        widest = max((col_name, col_value, ), key=lambda x: len(str(x)))
        return round(len(str(widest)) * 10 + len(str(widest)) * 0.45)

    def register_row_click(self, callback):
        """Registers callback for item click. Calls with item ID, which is first element in column by default"""
        self.double_click_callback = callback


    def _on_double_click(self, event):
        item = self.tree.identify_row(event.y)
        if item and self.double_click_callback:
            self.double_click_callback(item.iid)

    def populate(self, valuess: List[List[Any]], id_index: int):
        """Populates table with provided values, uses values[id_index] as id
        which used in row_click callback if such has been set"""
        self.tree.delete(*self.tree.get_children())
        for values in valuess:
            self.tree.insert('', 'end', iid=str(values[id_index]), values=values)


class PersonBaseDetailAppView(tk.Toplevel):
    # TODO: Organs are different for donor and acceptor, should be moved to a mixin?..
    #def __init__(self, parent, person, photo, organs, on_save):
    def __init__(self, parent, person, labels, values, photo, on_save=None):
        super().__init__(parent)
        self.person = person
        self.on_save = on_save
        self.title("Details for " + person.name)

        self.entries = {}
        fields = ["name", "birthdate", "blood_type", "gender", "height", "weight", "phone", "address", "notes"]
        for i, field in enumerate(fields):
            ttk.Label(self, text=field.capitalize()).grid(row=i, column=0, sticky='e')
            entry = ttk.Entry(self)
            entry.insert(0, str(getattr(acceptor, field) or ""))
            entry.grid(row=i, column=1)
            self.entries[field] = entry

        # # Organs
        # self.organ_listbox = tk.Listbox(self)
        # self.organ_listbox.grid(row=0, column=2, rowspan=6)
        # for o in organs:
        #     self.organ_listbox.insert(tk.END, o.organ_name)
        # ttk.Button(self, text="Add Organ", command=self.add_organ).grid(row=6, column=2)
        # ttk.Button(self, text="Remove Selected", command=self.remove_organ).grid(row=7, column=2)

        # Image preview
        self.image_label = ttk.Label(self)
        self.image_label.grid(row=8, column=2)
        self.photo_data = photo.photo if photo else None
        if self.photo_data:
            self.show_image()
        ttk.Button(self, text="Upload Photo", command=self.upload_photo).grid(row=9, column=2)

        ttk.Button(self, text="Save", command=self.save).grid(row=10, column=1)

    # def add_organ(self):
    #     name = tk.simpledialog.askstring("Organ", "Enter organ name:")
    #     if name:
    #         self.organ_listbox.insert(tk.END, name)

    # def remove_organ(self):
    #     for i in reversed(self.organ_listbox.curselection()):
    #         self.organ_listbox.delete(i)

    def upload_photo(self):
        path = ttk.filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png")])
        if path:
            with open(path, 'rb') as f:
                self.photo_data = f.read()
            self.show_image()

    def show_image(self):
        try:
            image = ttk.Image.open(io.BytesIO(self.photo_data))
            image.thumbnail((100, 100))
            self.tk_image = ttk.ImageTk.PhotoImage(image)
            self.image_label.configure(image=self.tk_image)
        except Exception as e:
            ttk.messagebox.showerror("Error", f"Invalid image: {e}")

    def save(self):
        try:
            self.person.name = self.entries["name"].get()
            self.person.birthdate = datetime.datetime.strptime(self.entries["birthdate"].get(), "%Y-%m-%d")
            self.person.blood_type = self.entries["blood_type"].get()
            self.person.gender = self.entries["gender"].get()
            self.person.height = int(self.entries["height"].get()) if self.entries["height"].get() else None
            self.person.weight = int(self.entries["weight"].get()) if self.entries["weight"].get() else None
            self.person.phone = self.entries["phone"].get()
            self.person.address = self.entries["address"].get()
            self.person.notes = self.entries["notes"].get()
            organs = list(self.organ_listbox.get(0, tk.END))
            self.on_save(self.person, self.photo_data, organs)
            self.destroy()
        except Exception as e:
            ttk.messagebox.showerror("Validation Error", str(e))