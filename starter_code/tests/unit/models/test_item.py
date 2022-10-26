from unittest import TestCase
from starter_code.models.item import ItemModel


class TestItem(TestCase):
    def test_create_item(self):
        item = ItemModel("test", 19.99)
        self.assertEqual(item.name, 'test', 'item name != constructed item name')
        self.assertEqual(item.price, 19.99, 'item price != constructed item price')

    def test_item_json(self):
        item = ItemModel("test", 19.99)
        expected = {'name': 'test', 'price': 19.99}
        actual = item.json()
        self.assertDictEqual(expected, actual, 'JSON exported by the item is not the expected '
                                               'Received: {} Expected {}'.format(actual, expected))

