from pathlib import Path
from unittest import TestCase
from wayfair.data_preprocessing.data_dao import *


class DataDAOTest(TestCase):

    def setUp(self):
        config.content_root = Path(__file__).parent

    def test_ordersDataDAO(self) -> None:
        self.assertIsNotNone(OrderDAO().dataframe)

    def test_paymentsDataDAO(self) -> None:
        self.assertIsNotNone(PaymentsDAO().dataframe)

    def test_featuresDataDAO(self) -> None:
        self.assertIsNotNone(FeatureDataDAO().dataframe)

    def test_zipcodeDataDAO(self) -> None:
        self.assertIsNotNone(ZipcodeDAO().dataframe)
