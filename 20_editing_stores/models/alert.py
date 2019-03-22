from dataclasses import dataclass, field
from typing import List, Dict
import uuid
from common.database import Database
from models.item import Item
from models.model import Model


@dataclass(eq=False)
class Alert(Model):
    collection: str = field(init=False, default="alerts")
    name: str
    item_id: str
    price_limit: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "price_limit": self.price_limit,
            "item_id": self.item._id
        }

    def load_item_price(self) -> float:
        self.item.load_price()
        return self.item.price

    def notify_if_price_reached(self) -> None:
        if self.item.price < self.price_limit:
            print(f"Item {self.item} has reached a price under {self.price_limit}. Latest price: {self.item.price}.")
