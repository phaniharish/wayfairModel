"""
Module for overall data preprocessing and feature extraction logic
"""
import pandas as pd

from wayfair.utils import *
from wayfair.data_preprocessing.data_dao import (
    OrderDAO,
    InventoryDAO,
    ZipcodeDAO,
    PaymentsDAO,
)


class FeatureExtractor:
    """
    A dataframe based feature extractor.

    The extractor uses the DAO objects to load the required data as dataframes.
    It extracts the features required for the model inference for each order and stores them in the data directory
    """

    def __init__(self):
        self.__orders_data = None
        self.__payments_data = None
        self.__inventory_data = None
        self.__zipcode_data = None

    @property
    def orders_data(self) -> pd.DataFrame:
        if not self.__orders_data:
            self.__orders_data = OrderDAO().dataframe
        return self.__orders_data

    @property
    def payments_data(self):
        if not self.__payments_data:
            self.__payments_data = PaymentsDAO().dataframe
        return self.__payments_data

    @property
    def inventory_data(self):
        if not self.__inventory_data:
            self.__inventory_data = InventoryDAO().dataframe
        return self.__inventory_data

    @property
    def zipcode_data(self):
        if not self.__zipcode_data:
            self.__zipcode_data = ZipcodeDAO().dataframe
        return self.__zipcode_data

    @staticmethod
    def add_payment_status(
        orders_data: pd.DataFrame, payments_data: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Function to merge payments and orders.

        :param orders_data: orders_data containing order_id
        :param payments_data: payments_data containing both order_id and payment_status
        :return: order_data containing payment_status
        """
        assert ("order_id" in payments_data.columns) and (
            "payment_status" in payments_data.columns
        )
        assert "order_id" in orders_data.columns

        orders_data_with_payment = pd.merge_asof(
            orders_data, payments_data, by="order_id", on=config.default_time_column
        )

        assert orders_data_with_payment.payment_status.isna().sum() == 0
        return orders_data_with_payment

    @staticmethod
    def add_inventory_info(orders_data: pd.DataFrame, inventory_data: pd.DataFrame):
        """
        Function to add inventory info for each order
        This can be easily achieved using the below liner, but adding a detailed
        approach for better demonstration
        ```
        pd.merge_asof(features, self.inventory_data,
                             on='timestamp', by='sku_code')
        ```
        :param orders_data:
        :param inventory_data:
        :return:
        """
        assert ("sku_code" in inventory_data.columns) and (
            "inventory" in inventory_data.columns
        )
        assert "sku_code" in orders_data.columns

        inventory_data.set_index(
            "sku_code", inplace=True
        )  # data already sorted by time
        orders_data["inventory"] = pd.NA  # set initial value to missing

        for i, row in orders_data.iterrows():
            inventory_info = inventory_data.loc[[row.sku_code]]
            inventory_info_order_time = inventory_info[
                (
                    inventory_info[config.default_time_column]
                    <= row[config.default_time_column]
                )
            ]
            inventory_info_order_time = inventory_info_order_time.sort_values(
                config.default_time_column
            )
            if (
                len(inventory_info_order_time.shape) > 0
                and inventory_info_order_time.shape[0] > 0
            ):
                # get most recent inventory status
                orders_data.at[i, "inventory"] = inventory_info.iloc[-1]["inventory"]

        assert orders_data["inventory"].isna().sum() == 0
        return orders_data

    @staticmethod
    def add_zipcode_data(
        orders_data: pd.DataFrame, zipcode_data: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Function to add zipcode data
        :param orders_data:
        :param zipcode_data:
        :return:
        """
        return orders_data.merge(zipcode_data, on=["zip_code"])

    @staticmethod
    def add_derivative_columns(features: pd.DataFrame):
        """

        :param features:
        :return:
        """
        features["zip_code_available"] = (
            features["timestamp"] > features["available_from"]
        )

        features["order_hour_of_day"] = features["timestamp"].dt.hour
        return features

    @staticmethod
    def store_features(feature_data):
        """

        :param feature_data:
        :return:
        """
        feature_data[
            [
                "order_id",
                "order_hour_of_day",
                "inventory",
                "payment_status",
                "zip_code_available",
            ]
        ].to_csv(config.features_data_path, index=False)
        logger.info("Storing features to path %s", config.features_data_path)

    def extract_features(self) -> pd.DataFrame:
        """

        :return:
        """
        orders_with_payments = self.add_payment_status(
            orders_data=self.orders_data, payments_data=self.payments_data
        )

        inventory_merged_features = self.add_inventory_info(
            orders_data=orders_with_payments, inventory_data=self.inventory_data
        )
        zipcode_merged_features = self.add_zipcode_data(
            orders_data=inventory_merged_features, zipcode_data=self.zipcode_data
        )
        feature_data = self.add_derivative_columns(zipcode_merged_features)
        required_features = feature_data[
            [
                "order_id",
                "order_hour_of_day",
                "inventory",
                "payment_status",
                "zip_code_available",
            ]
        ]
        required_features.set_index("order_id", inplace=True)
        required_features.to_csv(config.features_data_path)
        logger.info("Storing features to path %s", config.features_data_path)
        return required_features
