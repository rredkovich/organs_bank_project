import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import List, Any
from .utilities import calc_column_width


class BaseAppListView(ttk.Frame):
    def __init__(self, parent, controller, columns: List[str], double_click_callback=None):
        super().__init__(parent)
        self.table_columns = columns
        self.double_click_callback = double_click_callback
        self.controller = controller
        self.tree = ttk.Treeview(parent, show="headings")

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=3, column=1, sticky='ns')
        self.tree.grid(row=3, column=0)

        self.tree.bind('<Double-1>', self._on_double_click)

    def register_row_click(self, callback):
        """Registers callback for item click. Calls with item ID, which is first element in column by default"""
        self.double_click_callback = callback

    def _on_double_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if item_id and self.double_click_callback:
            self.double_click_callback(int(item_id))

    def populate(self, valuess: List[List[Any]], id_index: int = None):
        """Populates table with provided values, uses values[id_index] as id
        which used in row_click callback if such has been set"""
        self.tree.delete(*self.tree.get_children())
        self.tree['columns'] = self.table_columns
        for i, col in enumerate(self.table_columns):
            self.tree.column(i, width=calc_column_width(col, valuess[0][i] if valuess else 0), anchor='e')
            self.tree.heading(i, text=col)
        for values in valuess:
            if id_index is not None:
                self.tree.insert('', 'end', iid=str(values[id_index]), values=values)
            else:
                self.tree.insert('', 'end', values=values)


class PersonBaseDetailAppView(tk.Toplevel):
    INPUT_WIDTH = 20

    def __init__(self, parent, person, photo, choices, on_save):
        super().__init__(parent)
        self.person = person
        self.on_save = on_save
        self.title("Details for " + person.name)

        self.entries = {}
        fields = ["name", "birthdate", "blood_type", "gender", "height", "weight", "phone", "address", "notes"]
        for i, field in enumerate(fields):
            ttk.Label(self, text=field.capitalize()).grid(row=i, column=1, sticky='e')
            value = str(getattr(self.person, field) or "")
            if field == 'blood_type':
                widget = ttk.Combobox(self, values=choices['blood_types'], state='readonly', width=self.INPUT_WIDTH-2)
                widget.grid(row=i, column=2)
                widget.set(value=value)
            elif field ==  'gender':
                widget = ttk.Combobox(self, values=choices['genders'], state='readonly', width=self.INPUT_WIDTH-2)
                widget.grid(row=i, column=2)
                widget.set(value=value)
            else:
                widget = ttk.Entry(self, width=self.INPUT_WIDTH)
                widget.insert(0, str(getattr(self.person, field) or ""))

                widget.grid(row=i, column=2)
            self.entries[field] = widget

        # Image preview
        self.image_label = ttk.Label(self, width=20)
        self.image_label.grid(row=0, column=0, rowspan=len(fields))
        self.photo_data = photo.photo if photo else None
        if self.photo_data:
            self.show_image()
        ttk.Button(self, text="Upload Photo", command=self.upload_photo).grid(row=9, column=0)

        ttk.Button(self, text="Save", command=self.save).grid(row=9, column=2)

    def upload_photo(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png")])
        if path:
            with open(path, 'rb') as f:
                self.photo_data = f.read()
            self.show_image()

    def show_image(self):
        try:
            self.tk_image = tk.PhotoImage(data=self.photo_data)
            self.image_label.configure(image=self.tk_image)
            self.image_label.image = self.tk_image
        except Exception as e:
            messagebox.showerror("Error", f"Invalid image: {e}")

    def fetch_organs_list(self) -> List[Any]:
        raise NotImplemented("Implement in subclass")

    def save(self):
        try:
            self.person.name = self.entries["name"].get().strip()
            self.person.birthdate = datetime.datetime.strptime(self.entries["birthdate"].get().strip(), "%Y-%m-%d")
            self.person.blood_type = self.entries["blood_type"].get()
            self.person.gender = self.entries["gender"].get()
            self.person.height = int(self.entries["height"].get()) if self.entries["height"].get() else None
            self.person.weight = int(self.entries["weight"].get()) if self.entries["weight"].get() else None
            self.person.phone = self.entries["phone"].get()
            self.person.address = self.entries["address"].get()
            self.person.notes = self.entries["notes"].get()
            organs = self.fetch_organs_list()
            self.on_save(self.person, self.photo_data, organs)
            # self.destroy()
        except Exception as e:
            messagebox.showerror("Validation Error", str(e))


class ChoiceDialog(tk.simpledialog.Dialog):
    def __init__(self, parent, values: List[str], title='Choose an option'):
        self.options = values
        self.result = None
        super().__init__(parent, title)

    def body(self, master):
        self.combo = ttk.Combobox(master, values=self.options, state='readonly')
        self.combo.grid(row=0, column=0)
        self.combo.current(0)
        return self.combo  # initial focus

    def apply(self):
        self.result = self.combo.get()  # store chosen value