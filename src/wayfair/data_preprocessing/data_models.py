"""
Module to define specific dataclasses for each datatype
"""

from dataclasses import dataclass


@dataclass()
class Orders:
    order_id: str
    customer_id: str
    timestamp: str
    sku_code: str
    zip_code: str
    quantity: int = None
    order_fulfilled: str = None

