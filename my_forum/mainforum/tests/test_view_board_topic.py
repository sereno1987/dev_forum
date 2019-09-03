from django.test import TestCase
from django.urls import reverse, resolve
from ..views import home, board_topics, new_topics
from ..models import Boards, Topics,Posts, User

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

