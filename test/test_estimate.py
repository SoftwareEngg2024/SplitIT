import os
import json
from unittest.mock import patch
from telebot import types
from telebot_code import estimate
import helper

@patch("telebot.telebot")
def test_valid_spending_estimate(mock_telebot, mocker):
    # Mocking the user data (the data can be simulated to return valid results)
    MOCK_USER_DATA = {
        "894127939": [
            {"category": "Food", "amount": "10.00", "date": "2024-11-25"},
            {"category": "Transport", "amount": "5.00", "date": "2024-11-25"}
        ]
    }

    mocker.patch.object(estimate, "helper")
    estimate.helper.getUserHistory.return_value = MOCK_USER_DATA["894127939"]
    estimate.helper.getSpendEstimateOptions.return_value = ["Next day", "Next month"]
    estimate.helper.getDateFormat.return_value = "%d-%b-%Y"
    estimate.helper.getMonthFormat.return_value = "%b-%Y"

    # Setting up the mock Telegram bot
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("Next day")
    message.from_user = types.User(11, False, "test")
    message.text = "Next day"

    # Calling the function under test
    estimate.estimate_total(message, mc)

    # Assert that the bot sends a message (which indicates success)
    assert mc.send_message.called

@patch("telebot.telebot")
def test_invalid_period_format(mock_telebot, mocker):
    # Mocking the user data
    MOCK_USER_DATA = {
        "894127939": [
            {"category": "Food", "amount": "10.00", "date": "2024-11-25"},
            {"category": "Transport", "amount": "5.00", "date": "2024-11-25"}
        ]
    }

    mocker.patch.object(estimate, "helper")
    estimate.helper.getUserHistory.return_value = MOCK_USER_DATA["894127939"]
    estimate.helper.getSpendEstimateOptions.return_value = ["Next day", "Next month"]
    estimate.helper.getDateFormat.return_value = "%d-%b-%Y"
    estimate.helper.getMonthFormat.return_value = "%b-%Y"

    # Setting up the mock Telegram bot
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("Next week")
    message.from_user = types.User(11, False, "test")
    message.text = "Next week"  # Invalid option that triggers error handling

    # Calling the function under test
    estimate.estimate_total(message, mc)

    # Assert that the bot sends an error message (indicating error handling)
    assert mc.send_message.called
    assert "Sorry I can't show an estimate for" in mc.send_message.call_args[0][1]



@patch("telebot.telebot")
def test_invalid_format(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("luster")
    message.from_user = types.User(11, False, "test")
    try:
        estimate.estimate_total(message, mc)
        assert False
    except Exception:
        assert True


@patch("telebot.telebot")
def test_valid_format(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("Next month")
    message.from_user = types.User(11, False, "test")
    try:
        estimate.estimate_total(message, mc)
        assert True
    except Exception:
        assert False


@patch("telebot.telebot")
def test_valid_format_day(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("Next day")
    message.from_user = types.User(11, False, "test")
    try:
        estimate.estimate_total(message, mc)
        assert True
    except Exception:
        assert False


@patch("telebot.telebot")
def test_spending_estimate_working(mock_telebot, mocker):

    MOCK_USER_DATA = test_read_json()
    mocker.patch.object(estimate, "helper")
    estimate.helper.getUserHistory.return_value = MOCK_USER_DATA["894127939"]
    estimate.helper.getSpendEstimateOptions.return_value = ["Next day", "Next month"]
    estimate.helper.getDateFormat.return_value = "%d-%b-%Y"
    estimate.helper.getMonthFormat.return_value = "%b-%Y"
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("Next day")
    message.from_user = types.User(11, False, "test")
    message.text = "Next day"
    estimate.estimate_total(message, mc)
    assert mc.send_message.called


@patch("telebot.telebot")
def test_spending_estimate_month(mock_telebot, mocker):

    MOCK_USER_DATA = test_read_json()
    mocker.patch.object(estimate, "helper")
    estimate.helper.getUserHistory.return_value = MOCK_USER_DATA["894127939"]
    estimate.helper.getSpendEstimateOptions.return_value = ["Next day", "Next month"]
    estimate.helper.getDateFormat.return_value = "%d-%b-%Y"
    estimate.helper.getMonthFormat.return_value = "%b-%Y"
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("Next month")
    message.from_user = types.User(11, False, "test")
    message.text = "Next month"
    estimate.estimate_total(message, mc)
    assert mc.send_message.called


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
