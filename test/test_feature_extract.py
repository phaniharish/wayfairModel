from pathlib import Path
from unittest import TestCase

from wayfair.utils import config
from wayfair.data_preprocessing.feature_extraction import FeatureExtractor


class MyTestCase(TestCase):

    def setUp(self):
        config.content_root = Path(__file__).parent

    def test_feature_extract_init(self):
        self.assertGreater(FeatureExtractor().orders_data.shape[0], 0)

    def test_add_payment_status(self):
        fe = FeatureExtractor()
        res = fe.add_payment_status(fe.orders_data, fe.payments_data)
        self.assertEqual(res.payment_status.shape[0], 5)
        self.assertEqual(res.payment_status.value_counts().loc['OK'], 3)

    def test_add_inventory_info(self):
        fe = FeatureExtractor()
        res = fe.add_inventory_info(fe.orders_data, fe.inventory_data)
        self.assertEqual(res.inventory.shape[0], 5)
        self.assertEqual(res.inventory.loc[0], 63)

    def test_add_zipcode_data(self):
        fe = FeatureExtractor()
        res = fe.add_zipcode_data(fe.orders_data, fe.zipcode_data)
        self.assertEqual(res.zip_code.shape[0], 5)

    def test_extract_features(self):
        fe = FeatureExtractor()
        res = fe.extract_features()
