"""
    Tests about menu management
"""
import unittest

from flask import json

from . import ApiTestCase


class ItemModelCase(ApiTestCase):

    def test_items_post(self):
        self.assertEquals(
            self.client.post(self.init_data['RESTAURANT_CNAME'] + '/items',
                             headers={'Authorization': 'JWT ' + self.john_token},
                             data=json.dumps(dict(
                                title='Delicioso prato de batata',
                                price=10,
                                description='Batata rustica com amendoin e \
                                    alecrim e canela')),
                             content_type='application/json').status_code, 201)
        self.assertEquals(
            self.client.post(self.init_data['RESTAURANT_CNAME'] + '/items',
                             headers={'Authorization': 'JWT ' + self.karl_token},
                             data=json.dumps(dict(
                                title='Lentilhas com bardana',
                                price=12,
                                description='Lentilha cozida com raiz de bardana')),
                             content_type='application/json').status_code, 201)
        self.assertEquals(
            self.client.post(self.init_data['RESTAURANT_CNAME'] + '/items',
                             headers={'Authorization': 'JWT ' + self.susan_token},
                             data=json.dumps(dict(
                                title='Shitake',
                                price=13,
                                description='Sopa de cogumelos')),
                             content_type='application/json').status_code, 403)


if __name__ == '__main__':
    unittest.main(verbosity=2)
