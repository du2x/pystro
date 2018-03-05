"""
    Defines APIs for menu management.
"""
from flask_restful import Resource, reqparse

from sqlalchemy.exc import IntegrityError

from api.models.menu import Item, Section
from api.database import db
from api.auth import only_manager, current_identity
from api.utils import get_current_restaurant


titleArg = reqparse.Argument(name='title', type=str,
                             required=True,
                             help='title of item',
                             location='json')
descriptionArg = reqparse.Argument(name='description', type=str,
                                   required=True,
                                   help='description of item',
                                   location='json')
imgArg = reqparse.Argument(name='image_url', type=str,
                           required=False,
                           help='image of item',
                           location='json')
prcArg = reqparse.Argument(name='price', type=str,
                           required=True,
                           help='image of item',
                           location='json')


class ItemsAPI(Resource):
    """
    Defines routes for items listing and item adding.
    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(ItemsAPI, self).__init__()

    @only_manager()
    def post(self):
        self.reqparse.add_argument(titleArg)
        self.reqparse.add_argument(descriptionArg)
        self.reqparse.add_argument(imgArg)
        self.reqparse.add_argument(prcArg)
        data = self.reqparse.parse_args()
        try:
            item = Item(**data)
            item.created_by = current_identity.id
            item.restaurant_id = get_current_restaurant().id
            db.session.add(item)
            db.session.commit()
            return item.serializable(), 201
        except IntegrityError as e:
            db.session.rollback()
            return "Integrity error: " + str(e), 400


titleNotReqArg = titleArg
titleNotReqArg.required = False
descriptionNotReqArg = descriptionArg
descriptionNotReqArg.required = False
prcNotReqArg = prcArg
prcNotReqArg.required = False


class ItemAPI(Resource):
    """
    Defines routes for item editing and item viewing.
    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(titleNotReqArg)
        self.reqparse.add_argument(descriptionNotReqArg)
        self.reqparse.add_argument(prcNotReqArg)
        self.reqparse.add_argument(imgArg)
        super(ItemAPI, self).__init__()

    def get(self, id):
        item = Item.find_by_id(id)
        if not item:
            return "Item not found", 404
        else:
            return item.serializable(), 200

    @only_manager()
    def put(self, id):
        item = Item.find_by_id(id)
        if not item:
            return "Item not found", 404
        elif item.restaurant_id != get_current_restaurant().id:
            return "This section is not from this restaurant", 401
        else:
            data = self.reqparse.parse_args()
            for k, v in data.items():
                setattr(item, k, v)
            item.modified_by = current_identity.id
            db.session.add(item)
            db.session.commit()
            return item.serializable(), 200


class SectionsAPI(Resource):
    """
    Defines routes for items listing and item adding.
    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(SectionsAPI, self).__init__()

    @only_manager()
    def post(self):
        self.reqparse.add_argument(titleArg)
        self.reqparse.add_argument(descriptionArg)
        self.reqparse.add_argument(imgArg)
        data = self.reqparse.parse_args()
        try:
            sec = Section(**data)
            sec.created_by = current_identity.id
            db.session.add(sec)
            db.session.commit()
            return sec.serializable(), 201
        except IntegrityError as e:
            db.session.rollback()
            return "Integrity error: " + str(e), 400

    def get(self):
        return Section.find_all()


titleNotReqArg = titleArg
titleNotReqArg.required = False
descriptionNotReqArg = descriptionArg
descriptionNotReqArg.required = False


class SectionAPI(Resource):
    """
    Defines routes for section editing and item viewing.
    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(SectionAPI, self).__init__()

    def get(self, id):
        sec = Section.find_by_id(id)
        if not sec:
            return "Section not found", 404
        else:
            return sec.serializable(), 200

    @only_manager()
    def put(self, id):
        self.reqparse.add_argument(titleNotReqArg)
        self.reqparse.add_argument(descriptionNotReqArg)
        self.reqparse.add_argument(imgArg)
        sec = Section.find_by_id(id)
        if not sec:
            return "Section not found", 404
        elif sec.restaurant_id != get_current_restaurant().id:
            return "This section is not from this restaurant", 401
        else:
            data = self.reqparse.parse_args()
            for k in data.keys():
                setattr(sec, k, data[k])
            sec.modified_by = current_identity.id
            db.session.add(sec)
            db.session.commit()
            return sec.serializable(), 200


class MenuAPI(Resource):
    """
    Defines a get route for getting a structured menu data
    """

    def get(self):
        data = list()
        sections = Section.find_by_restaurant_id(get_current_restaurant().id)
        if sections:
            for section in sections:
                section_dict = dict()
                section_dict['title'] = section.title
                section_dict['items'] = list()
                for item in Item.find_by_section_id(section.id):
                    section_dict['items'].append(item.serializable())
                if section_dict['items']:
                    data.append(section_dict)
        return data, 200
