import tkinter as tk
import datetime
from tkinter import ttk, messagebox
from typing import List, Any
from .base_view import BaseAppListView, PersonBaseDetailAppView, ChoiceDialog
from .utilities import calc_column_width


class DonorListView(BaseAppListView):
    def __init__(self, parent, controller, columns, double_click_callback):
        super().__init__(parent, controller, columns, double_click_callback)


class DonorDetailsView(PersonBaseDetailAppView):
    def __init__(self, parent, donor, photo, on_save=None, organs=None,
                 choices={'organ_names': [], 'blood_types': [], 'genders': []}):
        super().__init__(parent, donor, photo, choices, on_save)

        self.choices = choices

        organs_tree = ttk.Treeview(self, show='headings')
        cols = ('organ name', 'extraction', 'expiration',)
        organs_tree['columns'] = cols
        organs_tree.grid(row=0, column=3, rowspan=6)
        for organ in organs:
            organs_tree.insert('', 'end', values=(organ.organ_name, organ.extraction_ts, organ.expiration_ts))

        for i, col in enumerate(cols):
            organs_tree.column(i, width=calc_column_width(col,1, multiplier=8), anchor='e')
            organs_tree.heading(i, text=col)

        self.organs_tree = organs_tree

        ttk.Button(self, text="Add Organ", command=self.add_organ).grid(row=7, column=3)
        ttk.Button(self, text="Remove Selected", command=self.remove_organ).grid(row=8, column=3)

    def add_organ(self):
        donated_organ = DonatedOrganDialog(self, self.choices['organ_names']).organ_pick_result
        if any(donated_organ):
            self.organs_tree.insert('', 'end', values=donated_organ)

    def remove_organ(self):
        selection = self.organs_tree.selection()
        self.organs_tree.delete(selection)

    def fetch_organs_list(self) -> List[Any]:
        return [self.organs_tree.item(item_id)['values'] for item_id in self.organs_tree.get_children()]


class DonatedOrganDialog(tk.simpledialog.Dialog):
    def __init__(self, parent, organ_values: List[str], title="Add donated organ"):
        self.options = organ_values
        self.organ_pick_result = None, None, None
        self.entries = {}
        super().__init__(parent, title)

    def body(self, parent):
        ttk.Label(parent, text="Organ").grid(row=0, column=3, sticky='w')
        self.combo = ttk.Combobox(parent, values=self.options, state='readonly')
        self.combo.grid(row=1, column=3)
        self.combo.current(0)
        fields = ['extraction', 'expiration']
        for i, field in enumerate(fields):
            ttk.Label(parent, text=field.capitalize()).grid(row=i, column=0, sticky='e')
            entry = ttk.Entry(parent)
            entry.insert(0, "")
            entry.grid(row=i, column=1)
            self.entries[field] = entry

    def apply(self):
        try:
            extraction = self.entries["extraction"].get().strip()
            expiration = self.entries["expiration"].get().strip()
            if expiration:
                expiration = datetime.datetime.strptime(expiration, '%Y-%m-%d').date()
            if extraction:
                extraction = datetime.datetime.strptime(extraction, '%Y-%m-%d').date()
        except Exception as e:
            messagebox.showerror("Validation Error", str(e))

        if extraction and expiration and (expiration < extraction):
            messagebox.showerror("Incorect date", "Expiration cannot be earlier than extraction")

        elif not extraction and not expiration:
            messagebox.showerror("Incorrect date", "At least one of extraction or expiration should be set")

        else:
            self.organ_pick_result = (
                self.combo.get(),
                extraction,
                expiration
            )
