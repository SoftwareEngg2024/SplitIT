from telebot_code import budget_update

# import mock
from unittest import mock
from unittest.mock import ANY
from unittest.mock import patch
from telebot import types


@patch("telebot.telebot")
def test_run_overall_budget_overall_case(mock_telebot, mocker):
    mc = mock_telebot.return_value

    mocker.patch.object(budget_update, "helper")
    budget_update.helper.isOverallBudgetAvailable.return_value = True

    budget_update.update_overall_budget = mock.Mock(return_value=True)
    message = create_message("hello from testing")
    message.from_user = types.User(11, False, "test")
    budget_update.run(message, mc)

    assert budget_update.update_overall_budget.called


@patch("telebot.telebot")
def test_run_overall_budget_category_case(mock_telebot, mocker):
    mc = mock_telebot.return_value

    mocker.patch.object(budget_update, "helper")
    budget_update.helper.isOverallBudgetAvailable.return_value = False
    budget_update.helper.isCategoryBudgetAvailable.return_value = True

    budget_update.update_category_budget = mock.Mock(return_value=True)
    message = create_message("hello from testing")
    message.from_user = types.User(11, False, "test")
    budget_update.run(message, mc)

    assert budget_update.update_category_budget.called


@patch("telebot.telebot")
def test_run_overall_budget_new_budget_case(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    mocker.patch.object(budget_update, "helper")
    budget_update.helper.isOverallBudgetAvailable.return_value = False
    budget_update.helper.isCategoryBudgetAvailable.return_value = False

    message = create_message("hello from testing")
    message.from_user = types.User(11, False, "test")
    budget_update.run(message, mc)

    assert mc.reply_to.called
    mc.reply_to.assert_called_with(message, "Select Budget Type", reply_markup=ANY)

@patch("telebot.telebot")
def test_post_type_selection_overall_budget_case(mock_telebot, mocker):
    mc = mock_telebot.return_value

    mocker.patch.object(budget_update, "helper")
    budget_update.helper.getBudgetTypes.return_value = {
        "overall": "Overall Budget",
        "category": "Category-Wise Budget",
    }

    budget_update.update_overall_budget = mock.Mock(return_value=True)
    message = create_message("Overall Budget")
    message.from_user = types.User(11, False, "test")
    budget_update.post_type_selection(message, mc)
    assert budget_update.update_overall_budget.called


@patch("telebot.telebot")
def test_post_type_selection_categorywise_budget_case(mock_telebot, mocker):
    mc = mock_telebot.return_value

    mocker.patch.object(budget_update, "helper")
    budget_update.helper.getBudgetTypes.return_value = {
        "overall": "Overall Budget",
        "category": "Category-Wise Budget",
    }

    budget_update.update_category_budget = mock.Mock(return_value=True)
    message = create_message("Category-Wise Budget")
    message.from_user = types.User(11, False, "test")
    budget_update.post_type_selection(message, mc)
    assert budget_update.update_category_budget.called


@patch("telebot.telebot")
def test_post_option_selectio_working(mock_telebot, mocker):
    mc = mock_telebot.return_value
    budget_update.update_category_budget = mock.Mock(return_value=True)

    message = create_message("Continue")
    message.from_user = types.User(11, False, "test")
    budget_update.post_option_selection(message, mc)

    assert budget_update.update_category_budget.called


@patch("telebot.telebot")
def test_post_option_selection_nonworking(mock_telebot, mocker):
    mc = mock_telebot.return_value
    budget_update.update_category_budget = mock.Mock(return_value=True)

    message = create_message("Randomtext")
    message.from_user = types.User(11, False, "test")
    budget_update.post_option_selection(message, mc)

    assert budget_update.update_category_budget.called is False

@patch("telebot.telebot")
def test_basic_response(mock_telebot):
    # Mock the bot instance
    mc = mock_telebot.return_value

    # Create a mock for a basic helper function
    budget_update.helper = mock.Mock()
    budget_update.helper.isOverallBudgetAvailable.return_value = True

    # Mock a function to be called in the test
    budget_update.update_overall_budget = mock.Mock(return_value=True)

    # Create a simple message
    message = create_message("Set my overall budget to $500")
    message.from_user = types.User(11, False, "TestUser")

    # Call the bot function directly
    budget_update.run(message, mc)

    # Ensure the mocked method was called
    assert budget_update.update_overall_budget.called

@patch("telebot.telebot")
def test_post_type_selection_invalid_case(mock_telebot, mocker):
    mc = mock_telebot.return_value

    # Mock helper function to return a set of valid budget types
    mocker.patch.object(budget_update, "helper")
    budget_update.helper.getBudgetTypes.return_value = {
        "overall": "Overall Budget",
        "category": "Category-Wise Budget",
    }

    # Mock a function to be called on invalid selection
    budget_update.update_category_budget = mock.Mock(return_value=True)

    # Create a message with an invalid selection
    message = create_message("Invalid Budget Type")
    message.from_user = types.User(11, False, "test")
    budget_update.post_type_selection(message, mc)

    # Ensure that no update occurs as the selection is invalid
    assert budget_update.update_category_budget.called is False

@patch("telebot.telebot")
def test_run_different_message(mock_telebot, mocker):
    mc = mock_telebot.return_value

    # Mock helper function to return True
    mocker.patch.object(budget_update, "helper")
    budget_update.helper.isOverallBudgetAvailable.return_value = True

    # Mock a function to be called when running the bot
    budget_update.update_overall_budget = mock.Mock(return_value=True)

    # Create a different message to test
    message = create_message("Set my budget to $1000 for the month")
    message.from_user = types.User(11, False, "test")
    
    # Call the bot function with the new message
    budget_update.run(message, mc)

    # Ensure the update function is called
    assert budget_update.update_overall_budget.called



def create_message(text):
    params = {"messagebody": text}
    chat = types.User(11, False, "test")
    message = types.Message(1, None, None, chat, "text", params, "")
    message.text = text
    return message
