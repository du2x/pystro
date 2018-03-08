from flask import request

from api.models.restaurant import Restaurant


def get_current_restaurant():
    cname = request.path.split('/')[1]
    rest = Restaurant.find_by_cname(cname)
    return rest
