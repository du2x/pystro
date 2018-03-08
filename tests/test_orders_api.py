"""
    Tests about orders management
"""
import unittest

from flask import json

from . import ApiTestCase


class OrdersModelCase(ApiTestCase):

    def test_orders(self):
        post_response = self.client.post(
                self.init_data['RESTAURANT_CNAME'] + '/orders',
                    headers={'Authorization': 'JWT ' + self.susan_token},
                    data=json.dumps(dict(
                    items=[{'id': 1, 'quantity': 1},
                           {'id': 2, 'quantity': 1}])),
                    content_type='application/json')
        order_id = json.loads(post_response.data)['id']
        self.assertEquals(post_response.status_code, 201)
        self.assertEquals(
            self.client.put(self.init_data['RESTAURANT_CNAME'] + '/orders',
                             headers={'Authorization': 'JWT ' + self.susan_token},
                             data=json.dumps({'order_id': order_id}),
                             content_type='application/json').status_code, 403)
        self.assertEquals(
            self.client.put(self.init_data['RESTAURANT_CNAME'] + '/orders',
                             headers={'Authorization': 'JWT ' + self.karl_token},
                             data=json.dumps({'order_id': order_id}),
                             content_type='application/json').status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)
