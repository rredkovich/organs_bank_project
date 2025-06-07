from app.models import AcceptorModel
from app.views import AcceptorAppDetailsView, AcceptorAppListVeiw

class AcceptorController:
    def __init__(self, parent):
        self.model = AcceptorModel()
        table_columns = self.model.field_names
        self.view = AcceptorAppListVeiw(parent, self, table_columns, self.open_detail)
        # self.view.pack(fill="both", expand=True)
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

    def open_detail(self, acceptor_id):
        acceptor, photo, organs = self.model.get_details(acceptor_id)
        AcceptorAppDetailsView(self.view, acceptor, photo, self.save, organs=organs, choices=self.model.possible_choices)

    def save(self, acceptor, photo, organs):
        self.model.save(acceptor, photo, organs)
        self.refresh()
