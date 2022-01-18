"""
A lightweight module to abstract the data access.
We currently just load the dataframe for each type of data to memory
"""

import pandas as pd
from wayfair.utils import *


class BaseDAO:
    """
    The base class has most of the data loading logic.
    The subclasses mainly exist to provide class speicifc config and for future
    extensibility with factory methods and special handling use cases.
    """

    def __init__(self, data_path, time_col=None):
        self.data_path = data_path
        self.time_col = time_col

        self._dataframe = None

    def load_data(self) -> pd.DataFrame:
        dataframe = pd.read_csv(self.data_path)
        if self.time_col:
            dataframe[self.time_col] = pd.to_datetime(dataframe[self.time_col])
            dataframe.sort_values(self.time_col, inplace=True)
        logger.info("Finished loading data from path %s", self.data_path)
        return dataframe

    @property
    def dataframe(self) -> pd.DataFrame:
        if not self._dataframe:
            self._dataframe = self.load_data()
        return self._dataframe


class OrderDAO(BaseDAO):
    def __init__(self):
        super().__init__(config.order_data_path, config.default_time_column)


class InventoryDAO(BaseDAO):
    def __init__(self):
        super().__init__(config.inventory_data_path, config.default_time_column)


class PaymentsDAO(BaseDAO):
    def __init__(self):
        super().__init__(config.payments_data_path, config.default_time_column)


class ZipcodeDAO(BaseDAO):
    def __init__(self):
        super().__init__(config.zipcode_data_path, config.zipcode_time_column)


class FeatureDataDAO(BaseDAO):
    def __init__(self):
        super().__init__(config.features_data_path)
