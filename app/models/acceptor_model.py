from typing import List
from datetime import datetime
from db import models as db
from .base_model import  BaseModel


class AcceptorModel(BaseModel):
    def __init__(self):
        super().__init__(db.Acceptor)

    def get_details(self, acceptor_id) -> (db.Acceptor, db.AcceptorPhoto, List[db.AwaitedOrgan],):
        acceptor = self.qs.fetch_one(acceptor_id, db.Acceptor)
        photo = self.qs.fetch_filtered('acceptor_id', acceptor_id, db.AcceptorPhoto)
        # TODO: temp hack
        if photo:
            photo = photo[0]
        organs = self.qs.fetch_filtered("acceptor_id", acceptor_id, db.AwaitedOrgan)
        return acceptor, photo, organs

    def create_new(self) -> db.Acceptor:
        return db.Acceptor(
            acceptor_id=0,
            name='',
            registration_date=datetime.now().date(),
            birthdate='',
            blood_type='',
            gender='',
            height='',
            weight='',
            phone='',
            address='',
            notes=''
        )

    def save(self, acceptor, photo, organs):
        self.qs.update_or_create(acceptor)
        if photo is not None:
            self.qs.update_or_create(db.AcceptorPhoto(acceptor.acceptor_id, photo))
        self.qs.delete_fitered(db.AwaitedOrgan, field='acceptor_id', value=acceptor.acceptor_id)
        for organ in organs:
            self.qs.create(db.AwaitedOrgan(acceptor.acceptor_id, organ))