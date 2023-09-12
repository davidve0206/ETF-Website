from django.test import TestCase
from .etfutils import tickers, risk_rating
from .models import BasicUser

# Create your tests here.

class TickersTestCase(TestCase):
    def test_tickers_are_complete(self):
        """ Test that get_tickers should return a list with 100 unique tickers """
        ticker_set = tickers.get_tickers()
        self.assertEqual(len(ticker_set), 100)

class RiskRatingTestCase(TestCase):
    def test_ratings_errors(self):
        """ Test that get_risk_ratings raises the right errors
            Using the right kwarg with values that are not accepted should raise a ValueError
            Using an invalid kwarg (ie. a Typo) should raise a TypeError """
        with self.assertRaises(ValueError):
            risk_rating.get_risk_rating(term="forever", obj="safeguard", absortion="low")
        with self.assertRaises(ValueError):
            risk_rating.get_risk_rating(term="short", obj="anything", absortion="low")
        with self.assertRaises(ValueError):
            risk_rating.get_risk_rating(term="short", obj="safeguard", absortion="none")

        with self.assertRaises(TypeError):
            risk_rating.get_risk_rating(tern="short", obj="safeguard", absortion="low")
        with self.assertRaises(TypeError):
            risk_rating.get_risk_rating(term="short", ovj="safeguard", absortion="low")
        with self.assertRaises(TypeError):
            risk_rating.get_risk_rating(term="short", obj="safeguard", avsortion="low")    


    def test_ratings_working(self):
        """ Testing the get_risk_ratings results are as expected """
        
        self.assertEqual(risk_rating.get_risk_rating(term="short", obj="safeguard", absortion="low"), 0)
        self.assertEqual(risk_rating.get_risk_rating(term="short", obj="safeguard", absortion="mid"), 0)
        self.assertEqual(risk_rating.get_risk_rating(term="short", obj="safeguard", absortion="high"), 0)
        self.assertEqual(risk_rating.get_risk_rating(term="short", obj="growth", absortion="low"), 0)
        self.assertEqual(risk_rating.get_risk_rating(term="short", obj="growth", absortion="mid"), 0)
        self.assertEqual(risk_rating.get_risk_rating(term="short", obj="growth", absortion="high"), 1)

        self.assertEqual(risk_rating.get_risk_rating(term="mid", obj="safeguard", absortion="low"), 0)
        self.assertEqual(risk_rating.get_risk_rating(term="mid", obj="safeguard", absortion="mid"), 0)
        self.assertEqual(risk_rating.get_risk_rating(term="mid", obj="safeguard", absortion="high"), 1)
        self.assertEqual(risk_rating.get_risk_rating(term="mid", obj="growth", absortion="low"), 0)
        self.assertEqual(risk_rating.get_risk_rating(term="mid", obj="growth", absortion="mid"), 1)
        self.assertEqual(risk_rating.get_risk_rating(term="mid", obj="growth", absortion="high"), 2)

        self.assertEqual(risk_rating.get_risk_rating(term="long", obj="safeguard", absortion="low"), 0)
        self.assertEqual(risk_rating.get_risk_rating(term="long", obj="safeguard", absortion="mid"), 1)
        self.assertEqual(risk_rating.get_risk_rating(term="long", obj="safeguard", absortion="high"), 1)
        self.assertEqual(risk_rating.get_risk_rating(term="long", obj="growth", absortion="low"), 1)
        self.assertEqual(risk_rating.get_risk_rating(term="long", obj="growth", absortion="mid"), 2)
        self.assertEqual(risk_rating.get_risk_rating(term="long", obj="growth", absortion="high"), 2)

class BasicUserModelTestCase(TestCase):
    """ Test for creating a user for the BasicUser Model"""
    def setUp(self) -> None:
        BasicUser.objects.create(email="test@test.com", name="test1", inv_term="mid", inv_objective="growth", loss_absortion="high")
        BasicUser.objects.create(email="test2@test.com", name="test2", inv_term="long", inv_objective="safeguard", loss_absortion="high")

    def test_user_gets_risk_rating(self):
        """ Test that creating a user gets the right risk_rating """
        user1 = BasicUser.objects.get(email="test@test.com")
        user2 = BasicUser.objects.get(email="test2@test.com")
        self.assertEqual(user1.risk_rating, 2)
        self.assertEqual(user2.risk_rating, 1)

    def test_user_gets_timestamp(self):
        """ Test that creating a user gets a timestamp """
        user1 = BasicUser.objects.get(email="test@test.com")
        user2 = BasicUser.objects.get(email="test2@test.com")
        self.assertIsNotNone(user1.last_update_date)
        self.assertIsNotNone(user2.last_update_date)