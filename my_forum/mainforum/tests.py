from django.test import TestCase
from django.urls import reverse, resolve
from .views import home, board_topics
from . models import Boards, Topics,Posts


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
        Board_to_topic_url = reverse("board_topics", kwargs={'pk': 1})
        response = self.client.get(Board_to_topic_url)
        home_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(home_url))

    # def test_new_topic_page_link_back_to_home_page(self):
    #     Board_to_new_topic_url = reverse("message_topics", kwargs={'pk': 1})
    #     response = self.client.get(Board_to_new_topic_url)
    #     home_url = reverse('home')
    #     self.assertContains(response, 'href="{0}"'.format(home_url))


class Board_topic_test(TestCase):
    def setUp(self):
        self.board = Boards.objects.create(name="Django", description="django framework")

    def test_board_topic_page_success_status(self):
        url = reverse('board_topics', kwargs={'pk':self.board.pk})
        result = self.client.get(url)
        self.assertEquals(result.status_code, 200)

    def test_board_topic_page_not_found_status(self):
        url = reverse('board_topics', kwargs={'pk':1000})
        result = self.client.get(url)
        self.assertEquals(result.status_code, 404)

    def test_board_topic_view_url(self):
        route = resolve("/boards/1")
        self.assertEquals(route.func, board_topics)



class New_topic_test(TestCase):
    def setUp(self):
        self.board = Boards.objects.create(name="Django", description="django framework")

    def test_new_topic_page_success_status(self):
        url = reverse('message_topics', kwargs={'pk':self.board.pk})
        result = self.client.get(url)
        self.assertEquals(result.status_code, 200)