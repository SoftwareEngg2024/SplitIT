import helper
import logging
from telebot import types
from db_operations import *


def run(message, bot):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if helper.isOverallBudgetAvailable(user_id):
        update_overall_budget(chat_id, user_id, bot)
    elif helper.isCategoryBudgetAvailable(user_id):
        update_category_budget(message, bot)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        options = helper.getBudgetTypes()
        markup.row_width = 2
        for c in options.values():
            markup.add(c)
        msg = bot.reply_to(message, "Select Budget Type", reply_markup=markup)
        bot.register_next_step_handler(msg, post_type_selection, bot)


def post_type_selection(message, bot):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        op = message.text
        options = helper.getBudgetTypes()
        if op not in options.values():
            bot.send_message(chat_id, "Invalid. Try again.")
            bot.register_next_step_handler(message, run, bot)
        else:
            if op == options["overall"]:
                update_overall_budget(chat_id, user_id, bot)
            elif op == options["category"]:
                update_category_budget(message, bot)
            else:
                bot.send_message(chat_id, "Something went wrong. Try again.")
                bot.register_next_step_handler(message, run, bot)

    except Exception as e:
        helper.throw_exception(e, message, bot, logging)


def update_overall_budget(chat_id, user_id, bot):
    if helper.isOverallBudgetAvailable(user_id):
        currentBudget = helper.getOverallBudget(user_id)
        msg_string = "Current Budget is ${}\n\nHow much is your new monthly budget? \n(Enter numeric values only)"
        message = bot.send_message(chat_id, msg_string.format(currentBudget))
    else:
        message = bot.send_message(
            chat_id, "How much is your monthly budget? \n(Enter numeric values only)"
        )
    bot.register_next_step_handler(message, post_overall_amount_input, bot)


def post_overall_amount_input(message, bot):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        amount_value = helper.validate_entered_amount(message.text)
        if amount_value == 0:
            bot.send_message(chat_id, "Invalid amount. Try again.")
            bot.register_next_step_handler(message, run, bot)
        else:
            userTransaction = read_user_transaction(user_id)

            if userTransaction == None:
                userTransaction = UserTransactions(telegram_user_id=user_id)
                create_user_transaction(userTransaction)

            userTransaction.budget["overall"] = amount_value
            update_user_transaction(user_id, userTransaction.to_dict())
            bot.send_message(chat_id, "Budget Updated!")
            return userTransaction
    except Exception as e:
        helper.throw_exception(e, message, bot, logging)


def update_category_budget(message, bot):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    categories = helper.getSpendCategories()
    markup.row_width = 2
    for c in categories:
        markup.add(c)
    msg = bot.reply_to(message, "Select Category", reply_markup=markup)
    bot.register_next_step_handler(msg, post_category_selection, bot)


def post_category_selection(message, bot):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        selected_category = message.text
        categories = helper.getSpendCategories()
        if selected_category not in categories:
            bot.send_message(chat_id, "Invalid. Try again.")
            bot.register_next_step_handler(message, run, bot)
        else:
            if helper.isCategoryBudgetByCategoryAvailable(user_id, selected_category):
                currentBudget = helper.getCategoryBudgetByCategory(
                    user_id, selected_category
                )
                msg_string = "Current monthly budget for {} is {}\n\nEnter monthly budget for {}\n(Enter numeric values only)"
                message = bot.send_message(
                    chat_id,
                    msg_string.format(
                        selected_category, currentBudget, selected_category
                    ),
                )
            else:
                message = bot.send_message(
                    chat_id,
                    "Enter monthly budget for "
                    + selected_category
                    + "\n(Enter numeric values only)",
                )
            bot.register_next_step_handler(
                message, post_category_amount_input, bot, selected_category
            )
    except Exception as e:
        helper.throw_exception(e, message, bot, logging)


def post_category_amount_input(message, bot, category):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        amount_value = helper.validate_entered_amount(message.text)
        if amount_value == 0:
            bot.send_message(chat_id, "Invalid. Try again.")
            bot.register_next_step_handler(message, run, bot)
        else:
            userTransaction = read_user_transaction(user_id)

            if userTransaction == None:
                userTransaction = UserTransactions(telegram_user_id=user_id)
                create_user_transaction(userTransaction)

            if userTransaction.budget["category"] is None:
                userTransaction.budget["category"] = {}
            userTransaction.budget["category"][category] = amount_value

            update_user_transaction(user_id, userTransaction.to_dict())
            message = bot.send_message(chat_id, "Budget for " + category + " Created!")
            post_category_add(message, bot)

    except Exception as e:
        helper.throw_exception(e, message, bot, logging)


def post_category_add(message, bot):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    options = helper.getUpdateOptions().values()
    markup.row_width = 2
    for c in options:
        markup.add(c)
    msg = bot.reply_to(message, "Select Option", reply_markup=markup)
    bot.register_next_step_handler(msg, post_option_selection, bot)


def post_option_selection(message, bot):
    print("here")
    selected_option = message.text
    options = helper.getUpdateOptions()
    print("here")
    if selected_option == options["continue"]:
        update_category_budget(message, bot)
