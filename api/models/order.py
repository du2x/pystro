"""
    Defines classes for Models for orders management
"""
from api.database import db
from api.models import BaseModel
from api.models.menu import Item


ORDER_PENDING=1
ORDER_CONFIRMED=2
ORDER_PAID=3
ORDER_CANCELED=4
ORDER_REJECTED=5


class Order(BaseModel):
    state = db.Column(db.Integer, default=ORDER_PENDING)
    expected_time_arrival = db.Column(db.DateTime)
    orderitems = db.relationship("OrderItem", backref="order")

    def total_price(self):
        if not self.orderitems:
            return 0
        return sum([orderitem.item.price * orderitem.quantity
                    for orderitem in self.orderitems])

    def serializable(self):
        return {'id': self.id, 'state': self.state,
                'total_price': self.total_price()}

    @classmethod
    def find_by_restaurant_id(cls, restaurant_id):
        result = cls.query.filter(cls.restaurant_id == restaurant_id)
        if result.count() > 0:
            return [order.serializable() for order in result]
        return []


class OrderItem(BaseModel):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    quantity = db.Column(db.Integer)
    item = db.relationship("Item")
