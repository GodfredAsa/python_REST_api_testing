from starter_code.models.item import ItemModel
from starter_code.models.store import StoreModel
from starter_code.tests.integration.integration_base_test import IntegrationBaseTest


class StoreTest(IntegrationBaseTest):
    def test_create_store(self):
        store = StoreModel("store")
        self.assertEqual(store.items.all(), [], "items is empty")

    def test_store_crud(self):
        with self.app_context():
            store = StoreModel("store")
            # store does not exist as not saved
            self.assertIsNone(StoreModel.find_by_name(store.name), "store does not exist")

            # store exists as its saved
            store.save_to_db()
            self.assertIsNotNone(StoreModel.find_by_name(store.name), "store exists")

            # store does not exist as deleted
            store.delete_from_db()
            self.assertIsNone(StoreModel.find_by_name(store.name), "store does not exist")

    def test_store_relationship_item(self):
        # NB store does not need the item but the item needs the store
        with self.app_context():
            store = StoreModel("store")
            item = ItemModel("test_item", 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, "test_item")

    # test store json with no item
    def test_store_json(self):
        store = StoreModel("store")
        expected = {"name": "store", "items": []}
        actual = store.json()
        self.assertDictEqual(expected, actual)

    def test_store_json_multiple_items(self):
        with self.app_context():
            store = StoreModel("store")
            item = ItemModel("test_item", 9.99, 1)
            store.save_to_db()
            item.save_to_db()
            expected = {"name": "store", "items": [{"name": "test_item", "price": 9.99}]}
            actual = store.json()
            self.assertDictEqual(expected, actual, "items in the store")

