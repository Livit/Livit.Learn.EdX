from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from labster.models import LabsterUser
from labster.users.admin import LabsterUserForm
from student.models import UserProfile


class LabsterUserFormTest(TestCase):

    def setUp(self):
        self.data = {
            'name': "First Last",
            'email': "new@user.com",
            'is_active': "1",
            'password': "password",
            'gender': "m",
            'level_of_education': "hs",
            'user_type': "2",
            'user_school_level': "5",
            'phone_number': "12345",
            'organization_name': "The Cool People",
            'nationality': "ID",
            'unique_id': "123123",
            'language': "en",
            'date_of_birth': str(date.today()),
        }

    def test_create_valid(self):
        data = {
            'name': "First Last",
            'email': "new@user.com",
        }

        form = LabsterUserForm(data)
        self.assertTrue(form.is_valid())

    def test_create_email_is_used(self):
        User.objects.create_user('new@user.com', 'new@user.com', 'user')

        data = {
            'name': "First Last",
            'email': "new@user.com",
        }

        form = LabsterUserForm(data)
        self.assertFalse(form.is_valid())

    def test_create_save(self):
        data = self.data.copy()

        form = LabsterUserForm(data)
        form.is_valid()
        labster_user = form.save()

        user = User.objects.get(id=labster_user.user.id)
        user_profile = UserProfile.objects.get(user=user)
        labster_user = LabsterUser.objects.get(user=user)

        self.assertEqual(user.email, data['email'])
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password(data['password']))

        self.assertEqual(user_profile.name, data['name'])
        self.assertEqual(user_profile.gender, data['gender'])
        self.assertEqual(user_profile.level_of_education, data['level_of_education'])

        self.assertEqual(labster_user.user_type, int(data['user_type']))
        self.assertEqual(labster_user.user_school_level, int(data['user_school_level']))
        self.assertEqual(labster_user.phone_number, data['phone_number'])
        self.assertEqual(labster_user.organization_name, data['organization_name'])
        self.assertEqual(labster_user.nationality, data['nationality'])
        self.assertEqual(labster_user.unique_id, data['unique_id'])
        self.assertEqual(labster_user.language, data['language'])
        self.assertEqual(str(labster_user.date_of_birth), data['date_of_birth'])

    def test_create_inactive(self):
        data = {
            'name': "First Last",
            'email': "new@user.com",
        }

        form = LabsterUserForm(data)
        form.is_valid()
        labster_user = form.save()
        user = User.objects.get(id=labster_user.user.id)

        self.assertFalse(user.is_active)

    def test_create_no_password(self):
        data = {
            'name': "First Last",
            'email': "new@user.com",
        }

        form = LabsterUserForm(data)
        form.is_valid()
        labster_user = form.save()
        user = User.objects.get(id=labster_user.user.id)

        self.assertFalse(user.has_usable_password())

    def test_update_valid(self):
        user = User.objects.create_user('new@user.com', 'new@user.com', 'user')
        labster_user = user.labster_user

        data = {
            'name': "First Last",
            'email': "other@user.com",
        }

        form = LabsterUserForm(data, instance=labster_user)
        self.assertTrue(form.is_valid())

    def test_update_save(self):
        user = User.objects.create_user('new@user.com', 'new@user.com', 'user')
        old_user_id = user.id
        labster_user = user.labster_user

        data = self.data.copy()

        form = LabsterUserForm(data, instance=labster_user)
        form.is_valid()
        labster_user = form.save()

        user = User.objects.get(id=labster_user.user.id)
        user_profile = UserProfile.objects.get(user=user)
        labster_user = LabsterUser.objects.get(user=user)

        self.assertEqual(user.id, old_user_id)

        self.assertEqual(user.email, data['email'])
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password(data['password']))

        self.assertEqual(user_profile.name, data['name'])
        self.assertEqual(user_profile.gender, data['gender'])
        self.assertEqual(user_profile.level_of_education, data['level_of_education'])

        self.assertEqual(labster_user.user_type, int(data['user_type']))
        self.assertEqual(labster_user.user_school_level, int(data['user_school_level']))
        self.assertEqual(labster_user.phone_number, data['phone_number'])
        self.assertEqual(labster_user.organization_name, data['organization_name'])
        self.assertEqual(labster_user.nationality, data['nationality'])
        self.assertEqual(labster_user.unique_id, data['unique_id'])
        self.assertEqual(labster_user.language, data['language'])
        self.assertEqual(str(labster_user.date_of_birth), data['date_of_birth'])

    def test_update_email_is_used(self):
        User.objects.create_user('other@user.com', 'other@user.com', 'user')
        user = User.objects.create_user('new@user.com', 'new@user.com', 'user')
        labster_user = user.labster_user

        data = {
            'name': "First Last",
            'email': "other@user.com",
        }

        form = LabsterUserForm(data, instance=labster_user)
        self.assertFalse(form.is_valid())

    def test_update_inactive(self):
        user = User.objects.create_user('new@user.com', 'new@user.com', 'user')
        labster_user = LabsterUser.objects.get(user=user)

        data = {
            'name': "First Last",
            'email': "new@user.com",
        }

        form = LabsterUserForm(data, instance=labster_user)
        form.is_valid()
        labster_user = form.save()
        user = User.objects.get(id=labster_user.user.id)

        self.assertFalse(user.is_active)

    def test_update_no_password(self):
        user = User.objects.create_user('new@user.com', 'new@user.com', 'user')
        labster_user = user.labster_user

        data = {
            'name': "First Last",
            'email': "new@user.com",
        }

        form = LabsterUserForm(data, instance=labster_user)
        form.is_valid()
        labster_user = form.save()
        user = User.objects.get(id=labster_user.user.id)

        self.assertFalse(user.has_usable_password())
