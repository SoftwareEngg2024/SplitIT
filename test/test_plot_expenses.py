# Import necessary libraries
import pytest
import pandas as pd
from telebot_code import expense_graph


# Test 1: Test that the function does not crash with empty dataframe
def test_input_does_not_crash():
    df = pd.DataFrame(columns=["name", "timestamp", "expense"])
    try:
        expense_graph.plot_expenses_with_histogram(df, granularity="day")
        assert True  # If no exception is raised, the test passes
    except Exception as E:
        assert False  # If exception is raised, the test fails


# Test 2: Test that the function works with a dataframe with missing values
def test_missing_values():
    df = pd.DataFrame(
        {
            "name": ["user1", "user2", "user3"],
            "timestamp": ["2024-11-23", "2024-11-23", "2024-11-23"],
            "expense": [10, None, 20],
        }
    )
    try:
        expense_graph.plot_expenses_with_histogram(df, granularity="day")
        assert True  # If no exception is raised, the test passes
    except Exception as E:
        assert False  # If exception is raised, the test fails


# Test 3: Test for future dates in the timestamp column
def test_future_dates():
    df = pd.DataFrame(
        {
            "name": ["user1", "user2"],
            "timestamp": ["2025-11-23", "2026-12-23"],
            "expense": [10, 20],
        }
    )
    try:
        expense_graph.plot_expenses_with_histogram(df, granularity="day")
        assert True  # If no exception is raised, the test passes
    except Exception as E:
        assert False  # If exception is raised, the test fails


# Test 4: Test granularity set to 'month'
def test_granularity_month():
    df = pd.DataFrame(
        {
            "name": ["user1", "user2"],
            "timestamp": ["2024-11-01", "2024-11-15"],
            "expense": [10, 20],
        }
    )
    try:
        expense_graph.plot_expenses_with_histogram(df, granularity="month")
        assert True  # If no exception is raised, the test passes
    except Exception as E:
        assert False  # If exception is raised, the test fails


# Test 5: Test multiple users on the same day
def test_multiple_users_one_day():
    df = pd.DataFrame(
        {
            "name": ["user1", "user2"],
            "timestamp": ["2024-11-23", "2024-11-23"],
            "expense": [10, 20],
        }
    )
    try:
        expense_graph.plot_expenses_with_histogram(df, granularity="day")
        assert True  # If no exception is raised, the test passes
    except Exception as E:
        assert False  # If exception is raised, the test fails


# Test 6: Test single user, single day scenario
def test_single_user_single_day():
    df = pd.DataFrame({"name": ["user1"], "timestamp": ["2024-11-23"], "expense": [10]})
    try:
        expense_graph.plot_expenses_with_histogram(df, granularity="day")
        assert True  # If no exception is raised, the test passes
    except Exception as E:
        assert False  # If exception is raised, the test fails


# Test 7: Test for duplicate entries
def test_duplicate_entries():
    duplicate_data = [
        {"name": "Alice", "userid": 1, "timestamp": "2024-11-01", "expense": 120},
        {
            "name": "Alice",
            "userid": 1,
            "timestamp": "2024-11-01",
            "expense": 120,
        },  # Duplicate
        {"name": "Bob", "userid": 2, "timestamp": "2024-11-02", "expense": 200},
    ]
    duplicate_df = pd.DataFrame(duplicate_data)
    duplicate_df["timestamp"] = pd.to_datetime(duplicate_df["timestamp"])
    duplicate_df_daywise = (
        duplicate_df.groupby(["name", duplicate_df["timestamp"].dt.date])["expense"]
        .sum()
        .reset_index()
    )
    duplicate_df_daywise["timestamp"] = pd.to_datetime(
        duplicate_df_daywise["timestamp"]
    )

    try:
        expense_graph.plot_expenses_with_histogram(
            duplicate_df_daywise, granularity="day"
        )
        assert True  # If no exception is raised, the test passes
    except Exception as E:
        assert False  # If exception is raised, the test fails


# Test 8: Test for missing timestamp data
def test_missing_timestamp_data():
    missing_timestamp_data = [
        {"name": "Alice", "userid": 1, "timestamp": "2024-11-01", "expense": 120},
        {
            "name": "Bob",
            "userid": 2,
            "timestamp": None,
            "expense": 200,
        },  # Missing timestamp
    ]
    missing_timestamp_df = pd.DataFrame(missing_timestamp_data)
    missing_timestamp_df["timestamp"] = pd.to_datetime(
        missing_timestamp_df["timestamp"], errors="coerce"
    )  # Coerce invalid dates to NaT
    missing_timestamp_df_daywise = (
        missing_timestamp_df.groupby(
            ["name", missing_timestamp_df["timestamp"].dt.date]
        )["expense"]
        .sum()
        .reset_index()
    )
    missing_timestamp_df_daywise["timestamp"] = pd.to_datetime(
        missing_timestamp_df_daywise["timestamp"]
    )

    try:
        expense_graph.plot_expenses_with_histogram(
            missing_timestamp_df_daywise, granularity="day"
        )
        assert True
    except Exception as E:
        assert False


# Test 9: Test for negative expense values
def test_negative_expense_values():
    negative_expense_data = [
        {
            "name": "Alice",
            "userid": 1,
            "timestamp": "2024-11-01",
            "expense": -50,
        },  # Negative expense
        {"name": "Bob", "userid": 2, "timestamp": "2024-11-02", "expense": 200},
    ]
    negative_expense_df = pd.DataFrame(negative_expense_data)
    negative_expense_df["timestamp"] = pd.to_datetime(negative_expense_df["timestamp"])
    negative_expense_df_daywise = (
        negative_expense_df.groupby(["name", negative_expense_df["timestamp"].dt.date])[
            "expense"
        ]
        .sum()
        .reset_index()
    )
    negative_expense_df_daywise["timestamp"] = pd.to_datetime(
        negative_expense_df_daywise["timestamp"]
    )

    try:
        expense_graph.plot_expenses_with_histogram(
            negative_expense_df_daywise, granularity="day"
        )
        assert True  # If no exception occurs, the test passes
    except Exception as E:
        assert False  # An exception is unexpected here


def test_single_user_valid_data_day():
    # Test with valid data for a single user with day granularity
    test_data = [
        {"userid": 1, "timestamp": "2024-11-01", "expense": 120},
        {"userid": 1, "timestamp": "2024-11-02", "expense": 90},
        {"userid": 1, "timestamp": "2024-11-03", "expense": 70},
    ]
    test_df = pd.DataFrame(test_data)
    test_df["timestamp"] = pd.to_datetime(test_df["timestamp"])

    try:
        expense_graph.plot_single_user_expenses(test_df, userid=1, granularity="day")
        assert True  # If no exception occurs, the test passes
    except Exception as e:
        assert False


def test_no_data_for_user():
    # Test with no data for the specified user
    test_data = [
        {"userid": 2, "timestamp": "2024-11-01", "expense": 120},
        {"userid": 2, "timestamp": "2024-11-02", "expense": 90},
    ]
    test_df = pd.DataFrame(test_data)
    test_df["timestamp"] = pd.to_datetime(test_df["timestamp"])

    try:
        expense_graph.plot_single_user_expenses(test_df, userid=1, granularity="day")
        assert True  # No exception is expected, but we need to ensure the user message is printed
    except Exception as e:
        assert False
