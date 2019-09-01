from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

class LoginRequiredPasswordChangeTest(TestCase):
    def test_redirection(self):
        url=reverse('password_change')
        login_url = reverse('login')
        response=self.client.get(url)
        # next will return the user to the page when he got the error
        self.assertRedirects(response,f'{login_url}?next={url}')

class PasswordChangeTest(TestCase):
    def setUp(self, data={}):
        self.user=User.objects.create_user(username="saba", email="saba@df.com", password="old_password")
        self.url = reverse('password_change')
        self.client.login(username="saba", password="old_password")
        self.response=self.client.post(self.url,data)

class SuccesssfulPasswordChangeTest(PasswordChangeTest):
    def setUp(self):
        super().setUp({
            "old_password":"old_password",
            "new_password1":"new_password",
            "new_password2":"new_password",
        })

    def test_redirection(self):
        """ after changing the password successfully the form shoould be redirected to another page"""
        print(self.response)
        self.assertRedirects(self.response,reverse('password_change_done'))

    def test_password_changed(self):
        """ get the new password by refreshing the db"""
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("new_password"))

    def test_user_authenticated(self):
       response = self.client.get(reverse('home'))
       user=response.context.get('user')
       self.assertTrue(user.is_authenticated)


class UnsuccesssfulPasswordChangeTest(PasswordChangeTest):
    def test_status_code(self):
        """ invalid form submisiion should be returned to the same page"""
        self.assertEqual(self.response.status_code,200)

    def test_form_errors(self):
        form=self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_didint_change_password(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("old_password"))

