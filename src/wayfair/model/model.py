"""
Module containing a model implementation(s) and `predict` function that can be invoked with a set of Features to get a
Recommendation
Example:
``
from model import Features, model_v1, predict
features = Features(...)
recommendation = predict(model_v1, features)
``
"""
from enum import Enum
from typing import Callable, NamedTuple

__all__ = [
    "Features",
    "Recommendation",
    "Model",
    "model_v1",
    "predict"
]


# Here we choose NamedTuple, but you can adapt this if you prefer to use # a dataclass or libraries like Pydantic (
# https://pydantic-docs.helpmanual.io/).


class Features(NamedTuple):
    """
    Container for model feature values
    :field: order_hour_of_day: int, A number between 0-23 with the hour of the day of the order timestamp
    :field: inventory: int, Sku inventory at the time of the order is placed
    :field: payment_status: str, Categorical feature: Payment status of the order returned by payment method provider
    :field: zip_code_available: bool, whether the delivery to the zip_code is possible """
    order_hour_of_day: int

    inventory: int
    payment_status: str
    zip_code_available: bool


class Recommendation(Enum):
    """
    Possible predicted classes
    """
    DELIVER = 'Deliver'
    HOLD_CHECK_AVAILABILITY = 'HoldCheckAvailability'
    HOLD_CHECK_DELIVERY = 'HoldCheckDelivery'
    HOLD_CHECK_PAYMENT = 'HoldCheckPayment'
    DECLINE = 'Decline'


# Signature for the model function. Not required, but feel free to adapt it or extend it
# if you need it for the next steps
Model = Callable[[Features], Recommendation]


def model_v1(features: Features) -> Recommendation:
    """
    This function is a very simple unrealistic example of what a
    decision tree could predict based on the example features above.
    We can assume that it behaves like a real-world ML model
    for the purposes of this exercise.
    """
    if features.inventory <= 0:
        return Recommendation.HOLD_CHECK_AVAILABILITY
    if not features.zip_code_available:
        return Recommendation.HOLD_CHECK_DELIVERY
    if features.payment_status != "OK":
        return Recommendation.HOLD_CHECK_PAYMENT
    if features.order_hour_of_day < 6:
        return Recommendation.DECLINE
    return Recommendation.DELIVER


def predict(model: Model, features: Features) -> Recommendation:
    """
    Invokes model with the given features to return a recommendation.
    Notice that model is a Callable that receives Features and returns Recommendation. """
    return model(features)
