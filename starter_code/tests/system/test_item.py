import json

from starter_code.models.item import ItemModel
from starter_code.models.store import StoreModel
from starter_code.models.user import UserModel
from starter_code.tests.base_test import BaseTest


class ItemTest(BaseTest):
    # def setUp(self) -> None:
    #     super(ItemTest, self).setUp() # calls the setup method of the base class
    #     with self.app() as client:
    #         with self.app_context():
    #             UserModel('test', '1234').save_to_db()
    #
    #             auth_request = client.post('/auth',
    #                                        data=json.dumps({'username': 'test', 'password': '1234'}),
    #                                        headers={'Content-Type': 'application/json'})
    #             auth_token = json.loads(auth_request.data)['access_token']
    #             self.access_token = f'JWT {auth_token}'


    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
               response = client.get('/item/test')
               self.assertEqual(401, response.status_code)

    # considerations for item not found with jwt_required
    # save a user
    # make a request to the auth endpoint with username and password
    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test', headers={'Authorization': self.access_token})
                self.assertEqual(404, response.status_code)

    def test_get_item_auth(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('store').save_to_db() # Postgres/MYSQL dont save a store, sqlite need to
                ItemModel('test', 19.9, 1).save_to_db()
                response = client.get('/item/test', headers={'Authorization': self.access_token})
                self.assertEqual(404, response.status_code)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('store').save_to_db()  # Postgres/MYSQL dont save a store, sqlite need to
                ItemModel('test', 19.9, 1).save_to_db()
                response = client.delete('/item/test')
                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'message': 'Item deleted'}, json.loads(response.data))


    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                # client.post('/store/my-store')
                StoreModel('store').save_to_db()
               # Postgres/MYSQL dont save a store, sqlite need to
                response = client.post('/item/test', data ={'price': 19.9, 'store_id': 1})
                print(response.data, " status code ")
                self.assertEqual(201, response.status_code)
                self.assertDictEqual({'name': 'test', 'price': 19.9}, json.loads(response.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('store').save_to_db()
                ItemModel('test', 19.9, 1).save_to_db()# Postgres/MYSQL dont save a store, sqlite need to
                response = client.post('/item/test', data={'price': 19.9, 'store_id': 1})
                self.assertEqual(400, response.status_code)
                self.assertDictEqual({'message': "An item with name \'test\' already exists."}, json.loads(response.data))

    # creates the item if item does not exist
    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('store').save_to_db()
                store_id = StoreModel.find_by_name('things').id
                response = client.put('/item/test', data={'price': 19.9, 'store_id': store_id})
                self.assertEqual(200, response.status_code)
                self.assertEqual(ItemModel.find_by_name('test').price, 19.9, 'compares if item is create with correct data')
                self.assertDictEqual({'name': 'test', 'price': 19.9}, json.loads(response.data))

    # updates the item if it exists
    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('store').save_to_db()
                ItemModel('test', 19.9,1)
                response = client.put('/item/test', data={'price': 200.99, 'store_id': 1})
                self.assertEqual(200, response.status_code)
                self.assertEqual(ItemModel.find_by_name('test').price, 200.9,
                                 'update the existing item')
                self.assertDictEqual({'name': 'test', 'price': 200.9}, json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                ItemModel('test', 19.9, 1).save_to_db()  # Postgres/MYSQL dont save a store, sqlite need to
                ItemModel('test-2', 69.9, 1).save_to_db()
                response = client.get('/items')
                self.assertEqual(200, response.status_code)
                self.assertDictEqual(
                    {'items':[
                        {'name': 'test', 'price': 19.9},
                        {'name': 'test-2', 'price': 69.9}
                    ]},json.loads(response.data)

                )

