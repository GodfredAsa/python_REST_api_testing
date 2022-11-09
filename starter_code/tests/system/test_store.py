import json

from starter_code.models.item import ItemModel
from starter_code.models.store import StoreModel
from starter_code.tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test')
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'name': 'test', 'items': []}, json.loads(response.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                response = client.post('/store/test')
                self.assertEqual(400, response.status_code)

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.delete('/store/test')
                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'message': 'Store deleted'}, json.loads(response.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.get('/store/test')
                self.assertEqual(200, response.status_code)
                self.assertDictEqual(
                    {'name': 'test', 'items': []}, json.loads(response.data)
                )

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/store/test')
                self.assertEqual(404, response.status_code)
                self.assertDictEqual({'message': 'Store not found'},
                                     json.loads(response.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.9, 1).save_to_db()
                response = client.get('/store/test')
                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'name': 'test',
                                      'items': [{'name': 'test', 'price': 19.9}]},
                                     json.loads(response.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                StoreModel('test-2').save_to_db()
                response = client.get('/stores')
                self.assertEqual(200, response.status_code)
                number_stores = len(json.loads(response.data)['stores'])
                self.assertEqual(2, number_stores)
                self.assertDictEqual({'stores': [{'name': 'test', 'items': []},
                                                 {'name': 'test-2', 'items': []}]},
                                     json.loads(response.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('store-1').save_to_db()
                ItemModel('item-1', 19.9, 1).save_to_db()

                StoreModel('store-2').save_to_db()
                ItemModel('items-2', 19.9, 2).save_to_db()

                response = client.get('/stores')
                self.assertEqual(200, response.status_code)
                number_stores = len(json.loads(response.data)['stores'])
                self.assertEqual(2, number_stores)
                print(json.loads(response.data))
                self.assertDictEqual({'stores': [
                    {'name': 'store-1', 'items': [{'name': 'item-1', 'price': 19.9}]},
                    {'name': 'store-2', 'items': [{'name': 'items-2', 'price': 19.9}]}]},
                    json.loads(response.data))



