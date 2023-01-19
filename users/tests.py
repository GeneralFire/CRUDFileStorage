from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Profile

# Create your tests here.


class UserNewUserTest(TestCase):

    USERNAME = 'USERNAME'
    PASSWORD = '123'

    def setUp(set):
        User.objects.create(
            username=UserNewUserTest.USERNAME,
            password=UserNewUserTest.PASSWORD
        )

    def test_correponding_profile(self):
        user = User.objects.get(
            username=UserNewUserTest.USERNAME
        )
        profile = Profile.objects.get(user=user)
        self.assertEqual(
            profile.user, user
        )


class UserDeleteUserTest(TestCase):

    USERNAME = 'USERNAME'
    PASSWORD = '123'

    def setUp(set):
        User.objects.create(
            username=UserDeleteUserTest.USERNAME,
            password=UserDeleteUserTest.PASSWORD
        )

    def test_correponding_profile(self):
        user = User.objects.get(
            username=UserDeleteUserTest.USERNAME
        )
        user.delete()
        with self.assertRaises(
            Profile.DoesNotExist,
        ):
            Profile.objects.get(user=user)
