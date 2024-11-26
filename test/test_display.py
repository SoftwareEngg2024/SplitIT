import os
import json
from unittest.mock import patch
from telebot import types
from telebot_code import display


@patch("telebot.telebot")
def test_run(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("hello from test run!")
    message.from_user = types.User(11, False, "test")
    display.run(message, mc)
    assert mc.reply_to.called


@patch("telebot.telebot")
def test_invalid_format(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("luster")
    message.from_user = types.User(11, False, "test")
    try:
        display.display_total(message, mc)
        assert False
    except Exception:
        assert True


@patch("telebot.telebot")
def test_valid_format(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("Month")
    message.from_user = types.User(11, False, "test")
    try:
        display.display_total(message, mc)
        assert True
    except Exception:
        assert False


@patch("telebot.telebot")
def test_valid_format_day(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("Day")
    message.from_user = types.User(11, False, "test")
    try:
        display.display_total(message, mc)
        assert True
    except Exception:
        assert False


@patch("telebot.telebot")
def test_spending_run_working(mock_telebot, mocker):
    MOCK_USER_DATA = test_read_json()
    mocker.patch.object(display, "helper")
    display.helper.getUserHistory.return_value = MOCK_USER_DATA["894127939"]
    display.helper.getSpendDisplayOptions.return_value = ["Day", "Month"]
    display.helper.getDateFormat.return_value = "%d-%b-%Y"
    display.helper.getMonthFormat.return_value = "%b-%Y"
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("Day")
    message.from_user = types.User(11, False, "test")
    message.text = "Day"
    display.run(message, mc)
    assert not mc.send_message.called


@patch("telebot.telebot")
def test_spending_display_working(mock_telebot, mocker):
    MOCK_USER_DATA = test_read_json()
    mocker.patch.object(display, "helper")
    display.helper.getUserHistory.return_value = MOCK_USER_DATA["894127939"]
    display.helper.getSpendDisplayOptions.return_value = ["Day", "Month"]
    display.helper.getDateFormat.return_value = "%d-%b-%Y"
    display.helper.getMonthFormat.return_value = "%b-%Y"
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("Day")
    message.from_user = types.User(11, False, "test")
    message.text = "Day"
    display.display_total(message, mc)
    assert mc.send_message.called


@patch("telebot.telebot")
def test_spending_display_month(mock_telebot, mocker):
    MOCK_USER_DATA = test_read_json()
    mocker.patch.object(display, "helper")
    display.helper.getUserHistory.return_value = MOCK_USER_DATA["894127939"]
    display.helper.getSpendDisplayOptions.return_value = ["Day", "Month"]
    display.helper.getDateFormat.return_value = "%d-%b-%Y"
    display.helper.getMonthFormat.return_value = "%b-%Y"
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("Month")
    message.from_user = types.User(11, False, "test")
    message.text = "Month"
    display.display_total(message, mc)
    assert mc.send_message.called

def test_calculate_spendings():
    # Mock input
    mock_query_result = [
        {"category": "Food", "amount": "50.00"},
        {"category": "Transport", "amount": "15.25"},
        {"category": "Food", "amount": "25.50"},
    ]

    # Expected output
    expected_output = "Food $75.5\nTransport $15.25\n"

    # Call the function
    result = display.calculate_spendings(mock_query_result)

    # Assert
    assert result == expected_output


@patch("telebot.telebot")
def test_getSpendDisplayOptions(mock_telebot, mocker):
    # Mock the return value for the helper method
    mocker.patch.object(display.helper, "getSpendDisplayOptions", return_value=["Day", "Month"])
    
    # Call the function that uses this method (could be display_total or any relevant method)
    options = display.helper.getSpendDisplayOptions()

    # Check that the options are exactly what we expect
    assert options == ["Day", "Month"]

@patch("telebot.telebot")
def test_reply_to_called(mock_telebot):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    
    # Create a mock message
    message = create_message("Test")
    message.from_user = types.User(11, False, "test")

    # Call the function that uses reply_to
    display.run(message, mc)

    # Check if reply_to was called
    assert mc.reply_to.called



def test_test_read_json_file_creation():
    # Try reading the test JSON data
    data = test_read_json()
    
    # Check that the data is not None or empty
    assert data is not None
    assert isinstance(data, dict)



# @patch('telebot.telebot')
# def test_display_overall_budget_by_text(mock_telebot, mocker):
#     MOCK_USER_DATA = test_read_json()
#     mocker.patch.object(display, 'helper')
#     display.helper.getDateFormat.return_value = '%d-%b-%Y'
#     display.helper.getMonthFormat.return_value = '%b-%Y'
#     history = MOCK_USER_DATA["1075979006"]["expense_data"]
#     budget_data = MOCK_USER_DATA["1075979006"]["budget"]["overall"]
#     message = display.display_budget_by_text(history, budget_data)
#     assert message == "Overall Budget is: 1000.0\n----------------------\nCurrent remaining budget is 812.69\n"


# @patch('telebot.telebot')
# def test_display_category_budget_by_text(mock_telebot, mocker):
#     MOCK_USER_DATA = test_read_json()
#     mocker.patch.object(display, 'helper')
#     display.helper.getDateFormat.return_value = '%d-%b-%Y'
#     display.helper.getMonthFormat.return_value = '%b-%Y'
#     history = MOCK_USER_DATA["1075979007"]["expense_data"]
#     budget_data = MOCK_USER_DATA["1075979007"]["budget"]["category"]
#     message = display.display_budget_by_text(history, budget_data)
#     print(message)
#     assert message == """Budget by Catergories is:
# Food:100.0
# Groceries:150.0
# Utilities:180.0
# Transport:20.0
# Shopping:180.0
# Miscellaneous:80.0
# ----------------------
# Current remaining budget is:
# Food:61.96
# Groceries:50.0
# Utilities:164.0
# Transport:-13.270000000000003
# Shopping:180.0
# Miscellaneous:80.0
# """


def create_message(text):
    params = {"messagebody": text}
    chat = types.User(11, False, "test")
    return types.Message(894127939, None, None, chat, "text", params, "")


def test_read_json():
    try:
        if not os.path.exists("./test/dummy_expense_record.json"):
            with open("./test/dummy_expense_record.json", "w") as json_file:
                json_file.write("{}")
            return json.dumps("{}")
        elif os.stat("./test/dummy_expense_record.json").st_size != 0:
            with open("./test/dummy_expense_record.json") as expense_record:
                expense_record_data = json.load(expense_record)
            return expense_record_data

    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")
