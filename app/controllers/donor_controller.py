from app.models import DonorModel
from app.views import DonorDetailsView, DonorListView

class DonorController:
    def __init__(self, parent):
        self.model = DonorModel()
        table_columns = self.model.field_names
        self.view = DonorListView(parent, self, table_columns, self.open_detail)
        self.refresh()

    def refresh(self):
        donors = self.model.get_all()
        id_index = 0
        fields = self.model.field_names
        valuess = []
        for donor in donors:
            values = [getattr(donor, field) for field in fields]
            valuess.append(values)

        self.view.populate(valuess, id_index)

    def open_detail(self, donor_id):
        donor, photo, organs = self.model.get_details(donor_id)
        DonorDetailsView(self.view, donor, photo, self.save, organs=organs, choices=self.model.possible_choices)

    def create_new(self):
        donor = self.model.create_new()
        photo = b''
        organs = []
        DonorDetailsView(self.view, donor, photo, self.save, organs=organs, choices=self.model.possible_choices)

    def save(self, donor, photo, organs):
        self.model.save(donor, photo, organs)
        self.refresh()
