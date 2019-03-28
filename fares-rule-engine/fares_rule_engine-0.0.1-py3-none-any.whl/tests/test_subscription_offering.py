import pytest

from fares import (
    is_subscription_offering_applicable_for_usage,
    SubscriptionOffering,
    is_subscription_offering_applicable_for_purchase,
)


@pytest.fixture
def subscription_offering_single_od_session():
    return {
        "id": "first_sub",
        "name": "Morning sub",
        "rides": "10",
        "currency": "INR",
        "validity_in_days": "20",
        "is_carry_forward": "True",
        "activation_date": "2019-02-28T12:56:41.589953+00:00",
        "deactivation_date": "2019-02-28T12:56:41.589953+00:00",
        "zone_id": "zone1",
        "amount": "1000",
        "subscription_type": "STANDARD",
        "applicability": [
            {
                "origin_cluster_id": "cluster_1",
                "destination_cluster_id": "cluster_2",
                "session": "MORNING",
            }
        ],
        "created_at": "2019-02-28T12:56:41.589953+00:00",
    }


@pytest.fixture
def subscription_offering_multiple_od_session():
    return {
        "id": "first_sub",
        "name": "Morning sub",
        "rides": "10",
        "currency": "INR",
        "validity_in_days": "20",
        "is_carry_forward": "True",
        "activation_date": "2019-02-28T12:56:41.589953+00:00",
        "deactivation_date": "2019-02-28T12:56:41.589953+00:00",
        "zone_id": "zone1",
        "amount": "1000",
        "subscription_type": "TRIAL",
        "applicability": [
            {
                "origin_cluster_id": "cluster_2",
                "destination_cluster_id": "cluster_1",
                "session": "MORNING",
            },
            {
                "origin_cluster_id": "cluster_2",
                "destination_cluster_id": "cluster_1",
                "session": "EVENING",
            },
        ],
        "created_at": "2019-02-28T12:56:41.589953+00:00",
    }


@pytest.fixture
def morning_slot():
    return {
        "origin_cluster_id": "cluster_1",
        "destination_cluster_id": "cluster_2",
        "session": "MORNING",
        "route_id": "route_id_1",
        "start_time": "2019-02-28T4:56:41.589953+00:00",
    }


@pytest.fixture
def evening_slot():
    return {
        "origin_cluster_id": "cluster_2",
        "destination_cluster_id": "cluster_1",
        "session": "EVENING",
        "route_id": "route_id_1",
        "start_time": "2019-02-28T12:56:41.589953+00:00",
    }


@pytest.fixture
def user_with_no_pass():
    return {"pass_purchase_count": 0, "id": "dummy_id", "gender": "MALE"}


@pytest.fixture
def user_with_pass():
    return {"pass_purchase_count": 1, "id": "dummy_id_2", "gender": "FEMALE"}


def test_is_offering_applicable_happy_single_od(
    subscription_offering_single_od_session, morning_slot
):
    assert is_subscription_offering_applicable_for_usage(
        SubscriptionOffering.from_json(subscription_offering_single_od_session),
        morning_slot,
    )


def test_is_offering_applicable_happy_multiple_od(
    subscription_offering_multiple_od_session, evening_slot
):
    assert is_subscription_offering_applicable_for_usage(
        SubscriptionOffering.from_json(subscription_offering_multiple_od_session),
        evening_slot,
    )


def test_is_offering_applicable_sad_multiple_od(
    subscription_offering_multiple_od_session, morning_slot
):
    assert not is_subscription_offering_applicable_for_usage(
        SubscriptionOffering.from_json(subscription_offering_multiple_od_session),
        morning_slot,
    )


def test_is_offering_applicable_for_purchase_trial_pass(
    subscription_offering_multiple_od_session, user_with_no_pass, user_with_pass
):
    assert is_subscription_offering_applicable_for_purchase(
        SubscriptionOffering.from_json(subscription_offering_multiple_od_session),
        user_with_no_pass,
    )

    assert not is_subscription_offering_applicable_for_purchase(
        SubscriptionOffering.from_json(subscription_offering_multiple_od_session),
        user_with_pass,
    )


def test_is_offering_applicable_for_purchase_standard_pass(
    subscription_offering_single_od_session, user_with_no_pass, user_with_pass
):
    assert is_subscription_offering_applicable_for_purchase(
        SubscriptionOffering.from_json(subscription_offering_single_od_session),
        user_with_no_pass,
    )

    assert is_subscription_offering_applicable_for_purchase(
        SubscriptionOffering.from_json(subscription_offering_single_od_session),
        user_with_pass,
    )
