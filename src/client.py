import datetime

from pydantic import BaseModel


class Address(BaseModel):
    city: str
    country: str
    state: str
    postal_code: str | None = None
    address: str | None = None
    district: str | None = None


class Contract(BaseModel):
    start: datetime.date
    end: datetime.date | None = None

    @property
    def is_active(self):
        return self.end is None or self.end > datetime.date.today()


class Client(BaseModel):
    id_: str
    name: str
    website: str | None = None
    google_drive_folder_id: str | None = None
    gov_id: str | None = None
    type_: str
    contract: Contract
    address: Address

    def __repr__(self):
        return f"Client {self.id_} - {self.name}"

    def __str__(self):
        return self.name

    @property
    def is_active(self):
        return self.contract.is_active
