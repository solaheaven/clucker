from django.core.exceptions import ValidationError
from django.test import TestCase
from microblogs.models import User

class UserModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('@johndoe',
            first_name = 'John',
            last_name = 'Doe',
            email = 'johndoe@gmail.com',
            password = 'Password123',
            bio = 'Hi, I am John.')

    def test_valid_user(self):
        self._assert_user_is_valid()
    
    def test_username_cannot_be_blank(self):
        self.user.username = ''
        self._assert_user_is_invalid()
    
    def test_username_can_be_30_characters_long(self):
        self.user.username = '@' + 'x' * 29
        self._assert_user_is_valid()
    
    def test_username_cannot_be_over_30_characters_long(self):
        self.user.username = '@' + 'x' * 30
        self._assert_user_is_invalid()
    
    def test_username_must_be_unique(self):
        User.objects.create_user('@janedoe',
            first_name = 'Jane',
            last_name = 'Doe',
            email = 'janedoe@gmail.com',
            password = 'Password123',
            bio = 'Hi, I am Jane.')
        self.user.username ='@janedoe'
        self._assert_user_is_invalid()
    
    def test_username_must_start_with_at_symbol(self):
        self.user.username ='johndoe'
        self._assert_user_is_invalid()
    
    def test_username_must_contin_only_alphanumericals_after_at(self):
        self.user.username ='@john!doe'
        self._assert_user_is_invalid()

    def test_username_must_contin_at_least_3_alphanumericals_after_at(self):
        self.user.username ='@jo'
        self._assert_user_is_invalid()

    def test_username_may_contain_numbers(self):
        self.user.username ='@j0hndoe2'
        self._assert_user_is_valid()
    
    def test_username_must_contin_only_one_at(self):
        self.user.username ='@@johndoe'
        self._assert_user_is_invalid()

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid.')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()