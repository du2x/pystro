"""
    Defines APIs for orders creation, confirmation and payment.
"""
from flask_restful import Resource, reqparse

from sqlalchemy.exc import IntegrityError

from api.models.order import Order, OrderItem, ORDER_PAID, \
                                     ORDER_PENDING
from api.database import db
from api.models.menu import Item
from api.auth import current_identity, only_manager, authenticated_user
from api.email import send_email
from api.utils import get_current_restaurant


class OrdersAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(OrdersAPI, self).__init__()

    @only_manager()
    def get(self):
        return Order.find_by_restaurant_id(get_current_restaurant().id)


    @authenticated_user()
    def post(self):
        """ creates an order """
        self.reqparse.add_argument('items', location='json', type=dict, action='append')
        data = self.reqparse.parse_args()
        try:
            order = Order()
            order.created_by = current_identity.id
            order.state = ORDER_PENDING
            rest = get_current_restaurant()
            order.restaurant_id = rest.id
            db.session.add(order)
            db.session.flush()
            for item in data['items']:
                order_item = OrderItem(order_id=order.id, item_id=int(item['id']),
                                       quantity=int(item['quantity']))
                dbitem = Item.find_by_id(item['id'])
                if dbitem.restaurant_id != order.restaurant_id:
                    raise IntegrityError
                db.session.add(order_item)
            db.session.commit()               
            send_email('New Order on Pystro!',
                       [mng.email for mng in rest.managers],
                       'Nice!')

            return order.serializable(), 201
        except IntegrityError as e:
            db.session.rollback()
            return "Integrity error: " + str(e), 400

    @only_manager()
    def put(self):
        """ confirms an order """
        self.reqparse.add_argument('order_id', type=int, location='json')
        data = self.reqparse.parse_args()
        try:
            order = Order.find_by_id(data['order_id'])
            if int(order.state) != ORDER_PENDING:
                return "Order is not pending", 401
            order.state = ORDER_PENDING
            db.session.add(order)
            db.session.commit()
            return order.serializable(), 200
        except IntegrityError as e:
            db.session.rollback()
            return "Integrity error: " + str(e), 400

    @only_manager()
    def patch(self):
        """ pays an order """
        try:
            self.reqparse.add_argument('order_id', type=int, location='json')
            data = self.reqparse.parse_args()
            order = Order.find_by_id(data['id'])
            if order.state != ORDER_PENDING:
                return "Order is not pending", 203
            order.state = ORDER_PAID
            db.session.add(order)
            db.session.commit()
            return order.serializable(), 200
        except IntegrityError as e:
            db.session.rollback()
            return "Integrity error: " + str(e), 400
