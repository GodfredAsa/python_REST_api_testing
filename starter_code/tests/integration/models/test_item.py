from starter_code.models.item import ItemModel
from starter_code.tests.base_test import BaseTest


class ItemTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            # step 1: SAVE an item
            item = ItemModel("test", 19.99)
            # ensure item not already in database
            self.assertIsNone(ItemModel.find_by_name('test'), 'item should not exit')
            # save item to db
            item.save_to_db()
            # assert item exist
            self.assertIsNotNone(ItemModel.find_by_name('test'),
                                 'found item with name: {} but should not'.format(item.name))

            # step 2: DELETE item from db
            item.delete_from_db()
            # ensure item not in database
            self.assertIsNone(ItemModel.find_by_name('test'),
                              'found item with name: {} but should not'.format(item.name))

            # step 3: UPDATE item price
