# Import necessary libraries
import pytest
import pandas as pd
from telebot_code import expense_graph

# Test 1: Test that the function does not crash with empty dataframe
def test_input_does_not_crash():
    df = pd.DataFrame(columns=['name', 'timestamp', 'expense'])
    try:
        expense_graph.plot_expenses_with_histogram(df, granularity='day')
        assert True  # If no exception is raised, the test passes
    except Exception as E:
        assert False  # If exception is raised, the test fails

# Test 2: Test that the function works with a dataframe with missing values
def test_missing_values():
    df = pd.DataFrame({
        'name': ['user1', 'user2', 'user3'],
        'timestamp': ['2024-11-23', '2024-11-23', '2024-11-23'],
        'expense': [10, None, 20]
    })
    try:
        expense_graph.plot_expenses_with_histogram(df, granularity='day')
        assert True  # If no exception is raised, the test passes
    except Exception as E:
        assert False  # If exception is raised, the test fails

# Test 3: Test for future dates in the timestamp column
def test_future_dates():
    df = pd.DataFrame({
        'name': ['user1', 'user2'],
        'timestamp': ['2025-11-23', '2026-12-23'],
        'expense': [10, 20]
    })
    try:
        expense_graph.plot_expenses_with_histogram(df, granularity='day')
        assert True  # If no exception is raised, the test passes
    except Exception as E:
        assert False  # If exception is raised, the test fails

