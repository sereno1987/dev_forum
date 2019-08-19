from django.test import TestCase
from django.urls import reverse, resolve
from .views import signup




class SignUp_test(TestCase):
    def setUp(self):
    #     self.board=acc.objects.create(name="Django", description="django framework")
        self.url = reverse('signup')
        self.response = self.client.get(self.url)

    def test_signup_view_success_status(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_view_url_match_func(self):
        route = resolve("/signup/")
        self.assertEquals(route.func, signup)

    def test_signup_link_back_to_home_page(self):
        signup_page = reverse("signup")
        response = self.client.get(signup_page)
        home_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(home_url))