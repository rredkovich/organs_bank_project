from typing import List
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

    def save(self, acceptor, photo, organs):
        self.qs.update(acceptor)
        if photo is not None:
            self.qs.update(db.AcceptorPhoto(acceptor.acceptor_id, photo))
        # self.qs.fetch_filtered("acceptor_id", acceptor.acceptor_id, db.AwaitedOrgan)  # remove old?
        # for organ in organs:
        #     self.qs.create(db.AwaitedOrgan(acceptor.acceptor_id, organ))