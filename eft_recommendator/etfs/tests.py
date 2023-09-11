from django.test import TestCase
from .EtfUtils import tickers, risk_rating

# Create your tests here.

class TickersTestCase(TestCase):
    def test_tickers_are_complete(self):
        """ get_tickers should return a list with 100 unique tickers """
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