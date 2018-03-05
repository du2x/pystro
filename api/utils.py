from flask import request

from api.models.restaurant import Restaurant


def get_current_restaurant():
    subdomain = request.path.split('/')[1]
    rest = Restaurant.find_by_subdomain(subdomain)
    return rest
