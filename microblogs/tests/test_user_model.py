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
#username
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
        second_user =self._create_second_user()
        self.user.username = second_user.username
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

#first name
    def test_first_name_cannot_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()

    def test_first_name_need_not_to_be_unique(self):
        second_user =self._create_second_user()
        self.user.first_name = second_user.first_name
        self._assert_user_is_valid()
    
    def test_first_name_may_contain_50_characters(self):
        self.user.first_name = 'x' * 50
        self._assert_user_is_valid()

    def test_first_name_may_not_contain_more_than_50_characters(self):
        self.user.first_name = 'x' * 51
        self._assert_user_is_invalid()
#last name
    def test_last_name_cannot_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()
        
    def test_last_name_need_not_to_be_unique(self):
        second_user =self._create_second_user()
        self.user.last_name = second_user.last_name
        self._assert_user_is_valid()
    
    def test_last_name_may_contain_50_characters(self):
        self.user.last_name = 'x' * 50
        self._assert_user_is_valid()

    def test_last_name_may_not_contain_more_than_50_characters(self):
        self.user.last_name = 'x' * 51
        self._assert_user_is_invalid()
#email

    def test_email_cannot_be_blank(self):
        self.user.email = ''
        self._assert_user_is_invalid()
        
    def test_email_need_to_be_unique(self):
        second_user =self._create_second_user()
        self.user.email= second_user.email
        self._assert_user_is_invalid()

    def test_email_must_contain_username(self):
        self.user.email = '@example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_at_symbol(self):
        self.user.email = 'johndoe.example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain_name(self):
        self.user.email = 'johndoe@.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain(self):
        self.user.email = 'johndoe@example'
        self._assert_user_is_invalid()
    
    def test_email_must_not_contain_more_than_one_at(self):
        self.user.email = 'johndoe@@example.org'
        self._assert_user_is_invalid()
#bio
    def test_bio_may_be_blank(self):
        self.user.bio= ''
        self._assert_user_is_valid()
        
    def test_email_need_not_to_be_unique(self):
        second_user =self._create_second_user()
        self.user.bio= second_user.bio
        self._assert_user_is_valid()
    
    def test_bio_may_contain_520_characters(self):
        self.user.bio= 'x' * 520
        self._assert_user_is_valid()

#basic
    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid.')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()
    
    def _create_second_user(self):
        user = User.objects.create_user('@janedoe',
            first_name = 'Jane',
            last_name = 'Doe',
            email = 'janedoe@gmail.com',
            password = 'Password123',
            bio = 'Hi, I am Jane.')
        return user