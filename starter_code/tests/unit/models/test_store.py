
from starter_code.models.store import StoreModel
from starter_code.tests.unit.unit_base_test import UnitBaseTest


class StoreTest(UnitBaseTest):

    def test_create_store(self):
        store = StoreModel("test_store")
        self.assertIsNotNone(store, "Store is not created or exists")
        self.assertEqual(store.name, "test_store",
                         "store name [{}] not same as constructed name: "
                         .format(store.name))



