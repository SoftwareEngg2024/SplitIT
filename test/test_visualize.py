import pytest
from unittest import mock
import matplotlib.pyplot as plt
from visualize import grp_exp_plot, income_plot, expense_plot  # Replace 'visualize' with your actual module name

def test_grp_exp_plot():
    with mock.patch("matplotlib.pyplot.savefig") as mock_savefig:
        # Calling grp_exp_plot without worrying about file handling
        grp_exp_plot()
        mock_savefig.assert_called_once_with("./graphs/grp_expense_chart.pdf")

# Test 2: Test income_plot when no data is returned (None)
def test_income_plot_none_data():
    with mock.patch("visualize.read_user_transaction", return_value=None):  # Replace 'visualize' if needed
        with mock.patch("matplotlib.pyplot.savefig") as mock_savefig:
            income_plot("6619121674")
            mock_savefig.assert_not_called()

# Test 3: Test income_plot with mock data
def test_income_plot_with_data():
    mock_data = mock.Mock()
    mock_data.transactions = {
        "income_data": [
            {"amount": "100", "category": "Salary"},
            {"amount": "200", "category": "Freelance"}
        ]
    }
    with mock.patch("visualize.read_user_transaction", return_value=mock_data):  # Replace 'visualize' if needed
        with mock.patch("matplotlib.pyplot.savefig") as mock_savefig:
            income_plot("6619121674")
            mock_savefig.assert_called_once_with("./graphs/income_chart.pdf")

# Test 4: Test expense_plot when no data is returned (None)
def test_expense_plot_none_data():
    with mock.patch("visualize.read_user_transaction", return_value=None):  # Replace 'visualize' if needed
        with mock.patch("matplotlib.pyplot.savefig") as mock_savefig:
            expense_plot("6619121674")
            mock_savefig.assert_not_called()

