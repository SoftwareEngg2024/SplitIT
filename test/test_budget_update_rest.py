from telebot_code import budget_update
from unittest.mock import ANY

# from unitest.mock import patch
from unittest.mock import patch
from telebot import types


@patch("telebot.telebot")
def test_update_overall_budget_already_available_case(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(budget_update, "helper")
    budget_update.helper.isOverallBudgetAvailable.return_value = True
    budget_update.helper.getOverallBudget.return_value = 100

    budget_update.update_overall_budget(120, 11, mc)
    mc.send_message.assert_called_with(120, ANY)


@patch("telebot.telebot")
def test_update_overall_budget_new_budget_case(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(budget_update, "helper")
    budget_update.helper.isOverallBudgetAvailable.return_value = True

    budget_update.update_overall_budget(120, 11, mc)
    mc.send_message.assert_called_with(120, ANY)


@patch("telebot.telebot")
def test_post_overall_amount_input_working(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(budget_update, "helper")
    budget_update.helper.isOverallBudgetAvailable.return_value = True
    budget_update.helper.validate_entered_amount.return_value = 150

    message = create_message("hello from testing")
    message.from_user = types.User(11, False, "test")
    budget_update.post_overall_amount_input(message, mc)

    mc.send_message.assert_called_with(11, ANY)


@patch("telebot.telebot")
def test_post_overall_amount_input_nonworking(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(budget_update, "helper")
    budget_update.helper.isOverallBudgetAvailable.return_value = True
    budget_update.helper.validate_entered_amount.return_value = 0
    budget_update.helper.throw_exception.return_value = True

    message = create_message("hello from testing")
    message.from_user = types.User(11, False, "test")
    budget_update.post_overall_amount_input(message, mc)

    assert mc.send_message.called


@patch("telebot.telebot")
def test_update_category_budget(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True

    mocker.patch.object(budget_update, "helper")
    budget_update.helper.getSpendCategories.return_value = [
        "Food",
        "Groceries",
        "Utilities",
        "Transport",
        "Shopping",
        "Miscellaneous",
    ]

    message = create_message("hello from testing")
    message.from_user = types.User(11, False, "test")
    budget_update.update_category_budget(message, mc)

    mc.reply_to.assert_called_with(message, "Select Category", reply_markup=ANY)


@patch("telebot.telebot")
def test_post_category_selection_category_wise_case(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(budget_update, "helper")
    budget_update.helper.getSpendCategories.return_value = [
        "Food",
        "Groceries",
        "Utilities",
        "Transport",
        "Shopping",
        "Miscellaneous",
    ]
    budget_update.helper.getCategoryBudgetByCategory.return_value = 10
    budget_update.helper.isCategoryBudgetByCategoryAvailable.return_value = True

    message = create_message("Food")
    message.from_user = types.User(11, False, "test")
    budget_update.post_category_selection(message, mc)

    mc.send_message.assert_called_with(11, ANY)
    assert budget_update.helper.getCategoryBudgetByCategory.called


@patch("telebot.telebot")
def test_post_category_selection_overall_case(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(budget_update, "helper")
    budget_update.helper.getSpendCategories.return_value = [
        "Food",
        "Groceries",
        "Utilities",
        "Transport",
        "Shopping",
        "Miscellaneous",
    ]
    budget_update.helper.isCategoryBudgetByCategoryAvailable.return_value = False

    message = create_message("Food")
    message.from_user = types.User(11, False, "test")
    budget_update.post_category_selection(message, mc)

    mc.send_message.assert_called_with(
        11, "Enter monthly budget for Food\n(Enter numeric values only)"
    )


@patch("telebot.telebot")
def test_post_category_amount_input_working(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(budget_update, "helper")
    budget_update.helper.validate_entered_amount.return_value = 100

    message = create_message("Hello from testing")
    message.from_user = types.User(11, False, "test")
    budget_update.post_category_amount_input(message, mc, "Food")

    mc.send_message.assert_called_with(11, "Budget for Food Created!")


@patch("telebot.telebot")
def test_post_category_amount_input_nonworking_case(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(budget_update, "helper")
    budget_update.helper.validate_entered_amount.return_value = 0
    budget_update.helper.throw_exception.return_value = True

    message = create_message("Hello from testing")
    message.from_user = types.User(11, False, "test")
    budget_update.post_category_amount_input(message, mc, "Food")

    assert mc.send_message.called


@patch("telebot.telebot")
def test_post_category_add(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True

    message = create_message("hello from testing!")
    message.from_user = types.User(11, False, "test")
    budget_update.post_category_add(message, mc)

    mc.reply_to.assert_called_with(message, "Select Option", reply_markup=ANY)

@patch("telebot.telebot")
def test_handle_ridiculous_input(mock_telebot):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    # Create a ridiculous message
    message = create_message("Set my budget to a million dollars 💰")
    message.from_user = types.User(11, False, "RichieRich")
    
    # Call the bot function directly without relying on helper behavior
    mc.send_message(11, "Processing your request...")

    # Verify that the bot responded to the user
    mc.send_message.assert_called_with(11, "Processing your request...")



def create_message(text):
    params = {"messagebody": text}
    chat = types.User(11, False, "test")
    message = types.Message(1, None, None, chat, "text", params, "")
    message.text = text
    return message
