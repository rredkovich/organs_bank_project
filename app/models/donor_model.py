from typing import List
from datetime import datetime
from db import models as db
from .base_model import  BaseModel


class DonorModel(BaseModel):
    def __init__(self):
        super().__init__(db.Donor)

    def create_new(self) -> db.Donor:
        return db.Donor(
            donor_id=0,
            name='',
            registration_date=datetime.now().date(),
            birthdate='',
            blood_type='',
            possible_extraction=datetime.now().date(),
            gender='',
            height='',
            weight='',
            phone='',
            address='',
            notes=''
        )

    def get_details(self, donor_id) -> (db.Donor, db.DonorPhoto, List[db.DonatedOrgan],):
        donor = self.qs.fetch_one(donor_id, db.Donor)
        photo = self.qs.fetch_filtered('donor_id', donor_id, db.DonorPhoto)
        # TODO: temp hack
        if photo:
            photo = photo[0]
        organs = self.qs.fetch_filtered("donor_id", donor_id, db.DonatedOrgan)
        return donor, photo, organs

    def save(self, donor, photo, organs):
        self.qs.update_or_create(donor)
        if photo is not None:
            self.qs.update_or_create(db.DonorPhoto(donor.donor_id, photo))
        self.qs.delete_fitered(db.DonatedOrgan, field='donor_id', value=donor.donor_id)
        for organ in organs:
            self.qs.create(db.DonatedOrgan(donor.donor_id, *organ))