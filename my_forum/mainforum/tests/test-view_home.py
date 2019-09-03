from django.test import TestCase
from django.urls import reverse, resolve
from ..views import home, board_topics, new_topics
from ..models import Boards, Topics,Posts, User


class Home_test(TestCase):
    def setUp(self):
        self.board=Boards.objects.create(name="Django", description="django framework")
        self.url = reverse('home')
        self.response = self.client.get(self.url)

    def test_home_view_success_status(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_view_url_match_func(self):
        route = resolve("/home/")
        self.assertEquals(route.func, home)

    def test_home_link_to_topic_page(self):
        Board_to_topic_url = reverse("board_topics", kwargs={'pk':self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(Board_to_topic_url))

    def test_topic_page_link_back_to_home_page(self):
        Board_to_topic_url = reverse("board_topics", kwargs={'pk': self.board.pk})
        response = self.client.get(Board_to_topic_url)
        home_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(home_url))

