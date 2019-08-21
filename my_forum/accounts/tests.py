from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from my_forum.accounts.views import signup
from my_forum.accounts.forms import SignUpForm


class SignUp_test(TestCase):
    def setUp(self):
        self.url = reverse('signup')
        self.response = self.client.get(self.url)

    def test_signup_view_success_status(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_view_url_match_func(self):
        route = resolve("/signup/")
        self.assertEquals(route.func, signup)

    # def test_signup_link_back_to_home_page(self):
    #     signup_page = reverse("signup")
    #     response = self.client.get(signup_page)
    #     home_url = reverse('home')
    #     self.assertContains(response, 'href="{0}"'.format(home_url))

    def test_csrf(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_contains_form(self):
        form=self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)



class Successful_signUp_test(TestCase):
    def setUp(self):
        url = reverse('signup')
        data={
            'username':'sabahaghighi',
            'email':'saba@ghs.com',
            'password1':'1234567891',
            'password2':'123456789',
        }
        self.response=self.client.post(url,data)
        self.home_url=reverse('home')

    def test_redirect(self):
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists)

    def test_authentication(self):
        response=self.client.get(self.home_url)
        user=response.context.get('user')
        self.assertTrue(user.is_authenticated)

    def test_form_inputs(self):
        ''' 5 inputs: csrf, username.....'''
        self.assertContains(self.response, '<input',5)
        self.assertContains(self.response, 'type="password"',2)
        self.assertContains(self.response, 'type="email"',1)
        self.assertContains(self.response, 'type="text"',1)



class UnsSuccessful_signUp_test(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response=self.client.post(url,{})

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_error_form(self):
        form=self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_failed_user_creation(self):
        self.assertFalse(User.objects.exists())