import unittest
from mock import MagicMock
from menu_planning.models import Lunch, Dinner
from menu_planning.services.lunch_service import LunchService
from menu_planning.actions.lunch_generator import LunchGenerator


class TestLunchGenerator(unittest.TestCase):

    def setUp(self):
        self.lunch_service = LunchService()

    def test_valid(self):
        self.lunch_service.get_random = MagicMock(return_value=Lunch(id=1, days=1))
        self.lunch_service.get_by_id_and_menu_id = MagicMock(return_value=None)

        lunch_generator = LunchGenerator(1, lunch_days_left=2, dinner_days_left=2, lunch_service=self.lunch_service)

        assert lunch_generator.is_valid()

    def test_invalid_has_enough_days(self):
        self.lunch_service.get_random = MagicMock(return_value=Lunch(id=1, days=3))
        self.lunch_service.get_by_id_and_menu_id = MagicMock(return_value=None)

        lunch_generator = LunchGenerator(1, lunch_days_left=2, dinner_days_left=2, lunch_service=self.lunch_service)

        assert not lunch_generator.is_valid()

    def test_invalid_is_already_add(self):
        lunch = Lunch(id=1, days=1)
        self.lunch_service.get_random = MagicMock(return_value=lunch)
        self.lunch_service.get_by_id_and_menu_id = MagicMock(return_value=lunch)

        lunch_generator = LunchGenerator(1, lunch_days_left=2, dinner_days_left=2, lunch_service=self.lunch_service)

        assert not lunch_generator.is_valid()

    def test_invalid_can_have_related_dinner(self):
        self.lunch_service.get_random = MagicMock(return_value=Lunch(id=1, days=1, related_dinner_id=1))
        self.lunch_service.get_by_id_and_menu_id = MagicMock(return_value=None)

        lunch_generator = LunchGenerator(1, lunch_days_left=2, dinner_days_left=2, is_dinner_left=True,
                                         lunch_service=self.lunch_service)

        assert not lunch_generator.is_valid()

    def test_invalid_has_related_dinner_enough_days(self):
        lunch = Lunch(id=1, days=1, related_dinner_id=1)
        lunch.related_dinner = Dinner(id=1, days=3)
        self.lunch_service.get_random = MagicMock(return_value=lunch)
        self.lunch_service.get_by_id_and_menu_id = MagicMock(return_value=None)

        lunch_generator = LunchGenerator(1, lunch_days_left=2, dinner_days_left=2, lunch_service=self.lunch_service)

        assert not lunch_generator.is_valid()
