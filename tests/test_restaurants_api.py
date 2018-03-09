"""
    Tests about restaurant management
"""
import unittest

from flask import json

from . import ApiTestCase


class RestaurantModelCase(ApiTestCase):


    def test_restaurants_post(self):
        self.assertEquals(
            self.client.post('/admin/restaurants',
                             headers={'Authorization': 'JWT ' + self.john_token},
                             data=json.dumps(dict(
                                name='Gaules',
                                cname='gaules',
                                phone='31 99832171')),
                             content_type='application/json').status_code, 201)
        self.assertEquals(
            self.client.post('/admin/restaurants',
                             headers={'Authorization': 'JWT ' + self.susan_token},
                             data=json.dumps(dict(
                                name='Familia Paulista',
                                cname='familia-paulista',
                                phone='31 99832333')),
                             content_type='application/json').status_code, 403)

    def test_restaurants_put(self):
        self.assertEquals(
            self.client.put('/admin/restaurant/' + str(self.init_data['RESTAURANT_ID']),
                            headers={'Authorization': 'JWT ' + self.john_token},
                            data=json.dumps(dict(
                              name='O Almazén',
                              phone='31 33292052')),
                            content_type='application/json').status_code, 200)
        self.assertEquals(
            self.client.put('/admin/restaurant/' + str(self.init_data['RESTAURANT_ID']),
                            headers={'Authorization': 'JWT ' + self.susan_token},
                            data=json.dumps(dict(
                              name='A Almazén',
                              phone='31 33292052')),
                            content_type='application/json').status_code, 403)


if __name__ == '__main__':
    unittest.main(verbosity=2)
