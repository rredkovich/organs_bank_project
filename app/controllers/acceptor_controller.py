import tkinter as tk
from app.models import AcceptorModel
from app.views import AcceptorAppDetailsView, AcceptorAppListVeiw, AcceptorOrganMatchView


class AcceptorController:
    def __init__(self, parent):
        self.model = AcceptorModel()
        table_columns = self.model.field_names
        self.view_parent = parent
        self.view = AcceptorAppListVeiw(parent, self, table_columns, self.open_detail)
        self.refresh()

    def refresh(self):
        acceptors = self.model.get_all()
        id_index = 0
        fields = self.model.field_names
        valuess = []
        for acceptor in acceptors:
            values = [getattr(acceptor, field) for field in fields]
            valuess.append(values)

        self.view.populate(valuess, id_index)

    def create_new(self):
        acceptor = self.model.create_new()
        photo = b''
        organs = []
        AcceptorAppDetailsView(self.view, acceptor, photo, self.save, organs=organs, choices=self.model.possible_choices)

    def open_detail(self, acceptor_id):
        acceptor, photo, organs = self.model.get_details(acceptor_id)
        AcceptorAppDetailsView(self.view, acceptor, photo, self.save, organs=organs, on_match=self.find_match,
                               choices=self.model.possible_choices)

    def find_match(self, acceptor_id):
        matches = self.model.find_organs_match(acceptor_id)
        fields = self.model.match_fields_names
        valuess = []
        for match in matches:
            values = [getattr(match, field) for field in fields]
            valuess.append(values)

        match_root = tk.Tk()
        match_root.title("Found Matches")
        view = AcceptorOrganMatchView(match_root, self, fields, None)
        view.populate(valuess)

    def save(self, acceptor, photo, organs):
        self.model.save(acceptor, photo, organs)
        self.refresh()
