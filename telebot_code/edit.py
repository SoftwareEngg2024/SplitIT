import re
import helper
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from db_operations import *


def run(m, bot):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    options = helper.getIncomeOrExpense()
    markup.row_width = 2
    for c in options.values():
        markup.add(c)
    msg = bot.reply_to(m, "Edit Income or Expense History", reply_markup=markup)
    bot.register_next_step_handler(msg, select_income_or_expense_to_be_edited, bot)


def select_income_or_expense_to_be_edited(msg, bot):
    user_id = msg.from_user.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    selectedType = msg.text
    if selectedType == "Income":
        for c in helper.getUserIncomeHistory(user_id):
            str_date = "Date=" + c["date"]
            str_category = ",\t\tCategory=" + c["category"]
            str_amount = ",\t\tAmount=$" + c["amount"]
            markup.add(str_date + str_category + str_amount)
    else:
        for c in helper.getUserExpenseHistory(user_id):
            str_date = "Date=" + c["date"]
            str_category = ",\t\tCategory=" + c["category"]
            str_amount = ",\t\tAmount=$" + c["amount"]
            markup.add(str_date + str_category + str_amount)

    info = bot.reply_to(msg, "Select income/expense to be edited:", reply_markup=markup)
    bot.register_next_step_handler(
        info, select_category_to_be_updated, bot, selectedType
    )


def select_category_to_be_updated(m, bot, selectedType):
    info = m.text
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    selected_data = [] if info is None else info.split(",")
    for c in selected_data:
        markup.add(c.strip())
    choice = bot.reply_to(m, "What do you want to update?", reply_markup=markup)
    bot.register_next_step_handler(
        choice, enter_updated_data, bot, selected_data, selectedType
    )


def enter_updated_data(m, bot, selected_data, selectedType):
    choice1 = "" if m.text is None else m.text
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    if selectedType == "Income":
        for cat in helper.getIncomeCategories():
            markup.add(cat)
    else:
        for cat in helper.getSpendCategories():
            markup.add(cat)

    if "Date" in choice1:
        calendar, step = DetailedTelegramCalendar().build()
        bot.send_message(m.chat.id, "Select a new date")
        bot.send_message(m.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)

        @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
        def cal(c):
            result, key, step = DetailedTelegramCalendar().process(c.data)

            if not result and key:
                bot.edit_message_text(
                    f"Select {LSTEP[step]}",
                    c.message.chat.id,
                    c.message.message_id,
                    reply_markup=key,
                )
            elif result:

                edit_date(c.message, bot, selected_data, selectedType, result)

                bot.edit_message_text(
                    f"Date is updated: {result}",
                    c.message.chat.id,
                    c.message.message_id,
                )

    if "Category" in choice1:
        new_cat = bot.reply_to(m, "Please select the new category", reply_markup=markup)
        bot.register_next_step_handler(
            new_cat, edit_cat, bot, selected_data, selectedType
        )

    if "Amount" in choice1:
        new_cost = bot.reply_to(m, "Please type the new cost")
        bot.register_next_step_handler(
            new_cost, edit_cost, bot, selected_data, selectedType
        )


def edit_date(m, bot, selected_data, selectedType, result):
    new_date = str(helper.validate_entered_date(result))

    user_id = m.from_user.id
    user_transactions = helper.getUserData(user_id=user_id)

    data_edit = helper.getUserHistory(user_id, selectedType)
    for i in range(len(data_edit)):
        user_data = data_edit[i]
        selected_date = selected_data[0].split("=")[1]
        selected_category = selected_data[1].split("=")[1]
        selected_amount = selected_data[2].split("=")[1]
        if (
            user_data["date"] == selected_date
            and user_data["category"] == selected_category
            and user_data["amount"] == selected_amount[1:]
        ):
            data_edit[i]["date"] = new_date
            break
    if selectedType == "Income":
        user_transactions.transactions["income_data"] = data_edit
        update_user_transaction(user_id, user_transactions.to_dict())
    else:
        user_transactions.transactions["expense_data"] = data_edit
        update_user_transaction(user_id, user_transactions.to_dict())

    bot.reply_to(m, "Date is updated")


def edit_cat(m, bot, selected_data, selectedType):
    user_id = m.from_user.id
    user_transactions = helper.getUserData(user_id=user_id)

    data_edit = helper.getUserHistory(user_id, selectedType)
    new_cat = "" if m.text is None else m.text
    for i in range(len(data_edit)):
        user_data = data_edit[i]
        selected_date = selected_data[0].split("=")[1]
        selected_category = selected_data[1].split("=")[1]
        selected_amount = selected_data[2].split("=")[1]
        if (
            user_data["date"] == selected_date
            and user_data["category"] == selected_category
            and user_data["amount"] == selected_amount[1:]
        ):
            data_edit[i]["category"] = new_cat
            break

    if selectedType == "Income":
        user_transactions.transactions["income_data"] = data_edit
        update_user_transaction(user_id, user_transactions.to_dict())

    else:
        user_transactions.transactions["expense_data"] = data_edit
        update_user_transaction(user_id, user_transactions.to_dict())

    bot.reply_to(m, "Category is updated")


def edit_cost(m, bot, selected_data, selectedType):
    new_cost = "" if m.text is None else m.text
    user_id = m.from_user.id
    user_transactions = helper.getUserData(user_id=user_id)
    data_edit = helper.getUserHistory(user_id, selectedType)

    if helper.validate_entered_amount(new_cost) != 0:
        for i in range(len(data_edit)):
            user_data = data_edit[i]
            selected_date = selected_data[0].split("=")[1]
            selected_category = selected_data[1].split("=")[1]
            selected_amount = selected_data[2].split("=")[1]
            if (
                user_data["date"] == selected_date
                and user_data["category"] == selected_category
                and user_data["amount"] == selected_amount[1:]
            ):
                data_edit[i]["amount"] = new_cost
                break

        if selectedType == "Income":
            user_transactions.transactions["income_data"] = data_edit
            update_user_transaction(user_id, user_transactions.to_dict())
            bot.reply_to(m, "Income amount is updated")
        else:
            user_transactions.transactions["expense_data"] = data_edit
            update_user_transaction(user_id, user_transactions.to_dict())
            bot.reply_to(m, "Expense amount is updated")
    else:
        bot.reply_to(m, "The cost is invalid")
        return
