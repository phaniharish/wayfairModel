import pytest
from wayfair.model.model import Features, Recommendation, model_v1 as model


def default_features_happy(
        *,
        order_hour_of_day: int = 10,
        inventory: int = 100,
        payment_status: str = "OK",
        zip_code_available: bool = True
) -> Features:
    """
    Create Features with default values for testing purposes.
    Optionally user can override specific features values to create test cases.
     Default values will match the happy case where recommendation should be "DELIVER" """
    return Features(
        order_hour_of_day,
        inventory,
        payment_status,
        zip_code_available
    )


def test_check_availability_zero_or_negative_inventory():
    assert model(
        default_features_happy(inventory=0)
    ) == Recommendation.HOLD_CHECK_AVAILABILITY
    assert model(
        default_features_happy(inventory=-1)
    ) == Recommendation.HOLD_CHECK_AVAILABILITY


def test_check_availability_positive_inventory():
    assert model(
        default_features_happy(inventory=1)
    ) == Recommendation.DELIVER


def test_check_delivery_zip_code_not_available():
    assert model(
        default_features_happy(zip_code_available=False)
    ) == Recommendation.HOLD_CHECK_DELIVERY


def test_check_delivery_zip_code_available():
    assert model(
        default_features_happy(zip_code_available=True)
    ) == Recommendation.DELIVER


def test_check_payment_status_not_ok():
    assert model(
        default_features_happy(payment_status="FAILED")
    ) == Recommendation.HOLD_CHECK_PAYMENT
    assert model(
        default_features_happy(payment_status="VERIFY_ADDRESS")
    ) == Recommendation.HOLD_CHECK_PAYMENT
    assert model(
        default_features_happy(payment_status="VERIFY_BANK_DETAILS")
    ) == Recommendation.HOLD_CHECK_PAYMENT


def test_check_payment_status_ok():
    assert model(
        default_features_happy(payment_status="OK")
    ) == Recommendation.DELIVER


def test_decline_bad_hour_of_day():
    assert model(
        default_features_happy(order_hour_of_day=0)
    ) == Recommendation.DECLINE


def test_not_decline_good_hour_of_day():
    assert model(
        default_features_happy(order_hour_of_day=7)
    ) == Recommendation.DELIVER


if __name__ == "__main__":
    pytest.main()
