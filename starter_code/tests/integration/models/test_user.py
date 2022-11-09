from starter_code.models.user import UserModel
from starter_code.tests.base_test import IntegrationBaseTest


class UserTest(IntegrationBaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel("test", "password")

            self.assertIsNone(UserModel.find_by_name("test"), "fetches user by username ")
            self.assertIsNone(UserModel.find_by_id(1), "fetches user by user id")

            user.save_to_db()
            self.assertIsNotNone(UserModel.find_by_name("test"), "user is saved")

            # ensures the password is not saved as raw text but hashed
            print(user.password)
            self.assertNotEqual(user.password, "password", "saved password not hashed")




