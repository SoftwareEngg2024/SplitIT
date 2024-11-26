#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import telebot
import time
import helper
import edit
import history
import display
import estimate
import delete
import add
import budget
import category
import add_recurring
import add_group_exp
import pdf
import link
import re
import plot_graphs
from telebot.types import BotCommand
import ocr_scan
from datetime import datetime
import expense_graph
from jproperties import Properties
from email_utils import send_email  # Import the email utility
from db_operations import save_user_email, get_user_email  # Import both functions
from history import fetch_user_expenses, format_expenses  # For fetching and formatting expenses

import sys

configs = Properties()

with open('user.properties', 'rb') as read_prop:
    configs.load(read_prop)

api_token = str(configs.get('api_token').data)

bot = telebot.TeleBot(api_token)

telebot.logger.setLevel(logging.INFO)

option = {}


# Command: /email_summary
api_token = str(configs.get('api_token').data)
bot = telebot.TeleBot(api_token)

@bot.message_handler(commands=['email_summary'])
def email_summary(message):
    user_id = message.chat.id
    user_email = get_user_email(user_id)  # Check if email exists in the database

    if not user_email:  # If no email is found, prompt the user
        bot.reply_to(message, "No email is saved. Please provide your email address:")
        bot.register_next_step_handler(message, handle_email)
    else:
        # Ask if the user wants to update the email
        bot.reply_to(message, f"Your saved email is {user_email}. Do you want to update it? Reply 'yes' to update or 'no' to continue:")
        bot.register_next_step_handler(message, handle_email_update, user_email)

def handle_email_update(message, current_email):
    user_id = message.chat.id
    response = message.text.strip().lower()

    if response == 'yes':  # Prompt for a new email
        bot.reply_to(message, "Please provide your new email address:")
        bot.register_next_step_handler(message, handle_email)
    elif response == 'no':  # Send the report to the current email
        bot.reply_to(message, f"Sending the report to your saved email: {current_email}")
        send_expense_report(message, current_email)
    else:  # Handle invalid responses
        bot.reply_to(message, "Invalid response. Please type 'yes' or 'no':")
        bot.register_next_step_handler(message, handle_email_update, current_email)


def is_valid_email(email):
    """Validate the email format."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


def handle_email(message):
    user_id = message.chat.id
    user_email = message.text

    # Validate email format
    if not is_valid_email(user_email):
        bot.reply_to(message, "Invalid email format. Please try again:")
        bot.register_next_step_handler(message, handle_email)
        return

    # Save the email in the database
    save_user_email(user_id, user_email)
    bot.reply_to(message, "Thanks! Your email has been updated. Sending your report now...")

    # Send the expenditure report
    send_expense_report(message, user_email)


def send_expense_report(message, user_email):
    user_id = message.chat.id
    expenses = fetch_user_expenses(user_id)  # Fetch expenditures from the database
    if expenses is None:
        bot.reply_to(message, "Sorry, you have not made any transactions. Add a transaction to enable sending email reports")
    else:
        summary = format_expenses(expenses)  # Format expenses for email

        try:
            send_email(user_email, "Your Monthly Expenditures", summary)
            bot.reply_to(message, "Your expenditure report has been sent to your email!")
        except Exception as e:
            bot.reply_to(message, f"Failed to send the email: {e}")

# Define listener for requests by user
def listener(user_requests):
    for req in user_requests:
        if(req.content_type == 'text'):
            print("{} name:{} chat_id:{} \nmessage: {}\n".format(str(datetime.now()), str(req.chat.first_name), str(req.chat.id), str(req.text)))


bot.set_update_listener(listener)

    
@bot.callback_query_handler(func=lambda call: call.data.startswith('date_'))
def handle_calendar_selection(call):
    selected_date = call.data.split('_')[1]
    bot.send_message(call.message.chat.id, f"You selected the date: {selected_date}")

# defines how the /start and /help commands have to be handled/processed
@bot.message_handler(commands=['start', 'menu'])
def start_and_menu_command(m):
    global user_list
    chat_id = m.chat.id

    text_intro = "Welcome to MyExpenseBot - a simple solution to track your expenses, incomes and manage them ! \n Please select the options from below for me to assist you with: \n\n"
    commands = helper.getCommands()
    for c in commands:  # generate help text out of the commands dictionary defined at the top
        text_intro += "/" + c + ": "
        text_intro += commands[c] + "\n\n"
    bot.send_message(chat_id, text_intro)
    return True


# defines how the /new command has to be handled/processed
# function to add an expense
@bot.message_handler(commands=['add'])
def command_add(message):
    add.run(message, bot)


# function to add recurring expenses
@bot.message_handler(commands=['add_recurring'])
def command_add_recurring(message):
    add_recurring.run(message, bot)


# function to add group expenses
@bot.message_handler(commands=['add_group_exp'])
def command_add_recurring(message):
    add_group_exp.run(message, bot)


# function to return graphs
@bot.message_handler(commands=['visualize'])
def command_add_recurring(message):
    plot_graphs.run(message, bot)

    
# function to fetch expenditure history of the user
@bot.message_handler(commands=['history'])
def command_history(message):
    history.run(message, bot)


# function to edit date, category or cost of a transaction
@bot.message_handler(commands=['edit'])
def command_edit(message):
    edit.run(message, bot)


# function to display total expenditure
@bot.message_handler(commands=['display'])
def command_display(message):
    print(message.from_user)
    display.run(message, bot)


# function to estimate future expenditure
@bot.message_handler(commands=['estimate'])
def command_estimate(message):
    estimate.run(message, bot)


# handles "/delete" command
@bot.message_handler(commands=['delete'])
def command_delete(message):
    delete.run(message, bot)


@bot.message_handler(commands=['budget'])
def command_budget(message):
    budget.run(message, bot)

@bot.message_handler(commands=['category'])
def command_category(message):
    category.run(message, bot)

@bot.message_handler(commands=['pdf'])
def command_category(message):
    pdf.run(message, bot)

@bot.message_handler(commands=['expense_graph'])
def command_expense_graph(message):
    expense_graph.run(message, bot)

# function to link user
@bot.message_handler(commands=['link'])
def command_add_link(message):
    link.run(message, bot)

@bot.message_handler(commands=['scan'])
def command_scan(message):
    ocr_scan.run(message, bot)


# not used
def addUserHistory(user_id, user_record):
    global user_list
    if(not(str(user_id) in user_list)):
        user_list[str(user_id)] = []
    user_list[str(user_id)].append(user_record)
    return user_list

def set_bot_commands():
    commands = [
        BotCommand(command="/start", description="Start the bot"),
        BotCommand(command="/menu", description="Show the menu"),
        BotCommand(command="/add", description="Add an expense"),
        BotCommand(command="/add_recurring", description="Add recurring expense"),
        BotCommand(command="/add_group_exp", description="Add group expense"),
        BotCommand(command="/visualize", description="Visualize your expenses"),
        BotCommand(command="/history", description="View your expense history"),
        BotCommand(command="/edit", description="Edit an expense"),
        BotCommand(command="/display", description="Display total expenditure"),
        BotCommand(command="/estimate", description="Estimate future expenses"),
        BotCommand(command="/delete", description="Delete an expense"),
        BotCommand(command="/budget", description="Set or view your budget"),
        BotCommand(command="/category", description="Manage categories"),
        BotCommand(command="/pdf", description="Generate a PDF report"),
        BotCommand(command="/link", description="Link your account"),
        BotCommand(command="/email_summary", description="Send monthly summary via email"),
    ]
    bot.set_my_commands(commands)

# Call this function before starting the bot
set_bot_commands()


def main():
    try:
        set_bot_commands()
        bot.polling(non_stop=True)
    except Exception as e:
        logging.exception(str(e))
        time.sleep(3)
        print("Connection Timeout")


if __name__ == '__main__':
    main()
