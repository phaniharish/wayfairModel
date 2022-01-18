"""
A simple client to invoke the service and save the results
"""
import time
import requests
import pandas as pd
from wayfair.data_preprocessing.data_dao import OrderDAO
from wayfair.utils import *


def invoke_endpoint(row) -> dict:
    """
    Invoke endpoint with data in row and return result
    :param row:
    :return: If query successful result is returned else return item with NA recommendation
    """
    res = requests.post(config.service_url, json=row.to_dict())
    if res.ok:
        return res.json()
    else:
        return {'order_id': row['order_id'],
                'recommendation': pd.NA}


def wait_for_endpoint_availability():
    """
    Check and wait for endpoint to be available
    :return: True if endpoint becomes available in 60 seconds else False
    """
    start_time = time.time()
    # wait for a minute for the endpoint to be ready
    while(time.time() - start_time) < 60:
        res = requests.get(config.ping_url)
        if res.ok:
            return True
    return False


def run() -> None:
    """
    Entry point method which iterates over all orders in orders.csv and
    invokes the service for each row.
    :return:
    """
    orders_dao = OrderDAO()
    orders_dao.time_col = None
    orders_data_required_columns = orders_dao.dataframe[['order_id',
                                                         'customer_id', 'timestamp', 'sku_code', 'zip_code']]
    assert wait_for_endpoint_availability(),\
        "Service endpoint unavailable. Please check the container"

    logger.info("Service available starting inference")
    results = pd.DataFrame(orders_data_required_columns.apply(invoke_endpoint, axis=1).dropna().values.tolist())

    recommendation_value_counts = results.recommendation.value_counts()
    if recommendation_value_counts.sum() == orders_data_required_columns.shape[0]:
        logger.info("All inferences succeeded!")

    logger.info("Result stats: \n%s", recommendation_value_counts)
    logger.info("Deliver percentage: %s",
                100*recommendation_value_counts.loc['Deliver']/orders_data_required_columns.shape[0])
    results.to_json(config.result_data_path, lines=True, orient='records')
    logger.info("Finished saving results to %s", config.result_data_path)
