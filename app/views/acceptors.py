import tkinter as tk
from tkinter import ttk
from typing import List, Any

from .base_view import BaseAppListView, PersonBaseDetailAppView, ChoiceDialog


class AcceptorAppListVeiw(BaseAppListView):
    def __init__(self, parent, controller, columns, double_click_callback):
        super().__init__(parent, controller, columns, double_click_callback)


class AcceptorAppDetailsView(PersonBaseDetailAppView):
    def __init__(self, parent, acceptor, photo, on_save=None, organs=None,
                 choices={'organ_names': [], 'blood_types': [], 'genders': []}):
        super().__init__(parent, acceptor, photo, choices, on_save)

        self.choices = choices

        # Organs
        self.organ_listbox = tk.Listbox(self)
        self.organ_listbox.grid(row=0, column=3, rowspan=6)
        if organs:
            for o in organs:
                self.organ_listbox.insert(tk.END, o.organ_name)
        ttk.Button(self, text="Add Organ", command=self.add_organ).grid(row=7, column=3)
        ttk.Button(self, text="Remove Selected", command=self.remove_organ).grid(row=8, column=3)

    def add_organ(self):
        name = ChoiceDialog(self, self.choices['organ_names']).result
        if name:
            self.organ_listbox.insert(tk.END, name)

    def remove_organ(self):
        for i in reversed(self.organ_listbox.curselection()):
            self.organ_listbox.delete(i)

    def fetch_organs_list(self) -> List[Any]:
        return list(self.organ_listbox.get(0, tk.END))
