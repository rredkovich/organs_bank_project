from dataclasses import dataclass
from typing import Optional
from datetime import datetime

class BaseDT:
    ...

@dataclass
class Gender(BaseDT):
    gender: str

@dataclass
class BloodType:
    blood_type: str

@dataclass
class OrganName:
    organ_name: str

@dataclass
class Organ:
    id: str
    organ_name: str
    blood_type: str

@dataclass
class Donor:
    donor_id: int
    name: str
    registration_date: datetime
    birthdate: datetime
    blood_type: str
    possible_extraction: datetime
    gender: str
    height: Optional[int] = None
    weight: Optional[int] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None

@dataclass
class Acceptor:
    acceptor_id: int
    name: str
    registration_date: datetime
    birthdate: datetime
    blood_type: Optional[str]
    gender: str
    height: Optional[int] = None
    weight: Optional[int] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None

@dataclass
class DonorPhoto:
    donor_id: int
    photo: bytes

@dataclass
class AcceptorPhoto:
    acceptor_id: int
    photo: bytes

@dataclass
class DonatedOrgan:
    donor_id: int
    organ_name: str
    extraction_ts: datetime
    expiration_ts: Optional[datetime] = None

@dataclass
class OrganWaitingQueue:
    acceptor_id: int
    organ_name: Optional[str] = None
