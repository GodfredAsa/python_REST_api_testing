from starter_code.models.item import ItemModel
from starter_code.tests.unit.unit_base_test import UnitBaseTest


class TestItem(UnitBaseTest):
    def test_create_item(self):
        item = ItemModel("test", 19.99, 1)
        self.assertEqual(item.name, 'test', 'item name != constructed item name')
        self.assertEqual(item.price, 19.99, 'item price != constructed item price')
        self.assertEqual(item.store_id, 1)
        self.assertIsNone(item.store)

    def test_item_json(self):
        item = ItemModel("test", 19.99, 1)
        expected = {'name': 'test', 'price': 19.99}
        actual = item.json()
        self.assertDictEqual(expected, actual, 'JSON exported by the item is not the expected '
                                               'Received: {} Expected {}'.format(actual, expected))


