import pandas as pd

import matplotlib.pyplot as plt

import matplotlib.dates as mdates
from datetime import datetime
import add_group_exp
import db_operations
import ast
from telebot import types

read_json = add_group_exp.read_json


def run(message, bot):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Daywise")
    markup.add("Monthwise")
    msg = bot.reply_to(
        message,
        "Select if you want a daywise or a monthwise graph:",
        reply_markup=markup,
    )
    bot.register_next_step_handler(msg, monthwise_or_daywise_record, bot)


def monthwise_or_daywise_record(message, bot):
    if message.text == "Daywise":
        gran = "day"
        msg = bot.reply_to(
            message, "Enter the number of " + gran + "s you want to show on the graph"
        )
        bot.register_next_step_handler(msg, vis_graph_record, bot, gran)
    elif message.text == "Monthwise":
        gran = "month"
        msg = bot.reply_to(
            message, "Enter the number of " + gran + "s you want to show on the graph"
        )
        bot.register_next_step_handler(msg, vis_graph_record, bot, gran)
    else:
        msg = bot.reply_to(message, "Sorry, did not recognize the option. Try again.")
        bot.register_next_step_handler(msg, run, bot)


def vis_graph_record(message, bot, granularity):
    txt = message.text
    chid = message.chat.id
    if not txt.isnumeric():
        msg = bot.reply_to(
            message,
            "Sorry, please enter only a whole number. Enter the number of "
            + granularity
            + "s you want to show on the graph",
        )
        bot.register_next_step_handler(msg, vis_graph_record, bot, granularity)
    else:
        num_ele = int(txt)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Mine")
        markup.add("Group")
        msg = bot.reply_to(
            message,
            "Do you want to plot your expenses or group expenses?",
            reply_markup=markup,
        )
        bot.register_next_step_handler(
            msg, single_or_group_expenses, bot, granularity, num_ele
        )


def single_or_group_expenses(message, bot, granularity, ndays):
    chid = message.chat.id
    uid = message.from_user.id
    if message.text == "Mine":
        dfp = []
        det = db_operations.read_user_transaction(uid)
        if det == None:
            bot.send_message(chid, "No expenses made yet")
        else:
            exp = det.transactions["expense_data"]
            for rec in exp:
                record = {
                    "userid": uid,
                    "timestamp": rec["date"],
                    "expense": rec["amount"],
                }
                dfp.append(record)
            df = pd.DataFrame(dfp)
            F = plot_single_user_expenses(df, uid, granularity=granularity, ndays=ndays)
            bot.send_message(chid, "Here is your timeline of your expenses:")
            bot.send_photo(chid, F)
    elif message.text == "Group":
        det = read_json()

        if det == {} or not (str(uid) in det.keys()):
            bot.send_message(chid, "No group expenses made yet")
        else:
            df = conv_to_df(det[str(uid)]["expense"])
            F = plot_expenses_with_histogram(df, granularity=granularity, ndays=ndays)
            bot.send_message(chid, "Here is your timeline of your group expenses:")
            bot.send_photo(chid, F)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Mine")
        markup.add("Group")
        msg = bot.reply_to(
            message,
            "Only 2 options are available. Try again.\nDo you want to plot your expenses or group expenses?",
            reply_markup=markup,
        )
        bot.register_next_step_handler(
            msg, single_or_group_expenses, bot, granularity, ndays
        )


def conv_to_df(det):
    dfp = []
    for record in det:
        i1 = record.find("[")
        ml = record[i1:]
        member_list = ast.literal_eval(ml)
        member_list.append("You")
        expensedata = record[0 : i1 - 1].split(",")
        date = expensedata[0]
        dollaramt = expensedata[1]
        precord = {"timestamp": date, "expense": dollaramt, "name": "You"}
        dfp.append(precord)
        for name in member_list:
            pcopy = precord.copy()
            pcopy["name"] = name
            dfp.append(pcopy)
    final_rec = pd.DataFrame(dfp)
    return final_rec


def plot_expenses_with_histogram(df, granularity="day", ndays=0):
    users = df["name"].unique()
    df = df.astype({'expense':'float'})

    Y = ndays / 365
    M = ndays / 30 - Y * 12
    D = ndays - 30 * M

    fig, ax1 = plt.subplots(figsize=(12, 6))
    for user in users:
        user_data = df[df["name"] == user]
        L = len(user_data["timestamp"])
        if ndays == 0:
            ndays = L
        l = L - ndays

        ax1.plot(
            pd.to_datetime(user_data["timestamp"]),
            user_data["expense"],
            label=user,
            marker="o",
        )

    ax1.xaxis.set_major_locator(
        mdates.DayLocator() if granularity == "day" else mdates.MonthLocator()
    )
    ax1.xaxis.set_major_formatter(
        mdates.DateFormatter("%Y-%m-%d" if granularity == "day" else "%Y-%m")
    )

    fig.autofmt_xdate()

    ax1.set_xlabel(f"{granularity.capitalize()}s")
    ax1.set_ylabel("Expense Amount (Per User)")

    ax2 = ax1.twinx()  # Create a twin Axes sharing the x-axis
    total_expenses_per_day = df.groupby("timestamp")["expense"].sum().reset_index()

    bars = ax2.bar(
        pd.to_datetime(total_expenses_per_day.iloc["timestamp"]),
        total_expenses_per_day["expense"],
        alpha=0.2,
        color="gray",
        width=0.8,
    )

    ax2.set_ylabel("Total Expenses (All Users)")

    for bar, total in zip(bars, total_expenses_per_day["expense"]):
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{total}",
            ha="center",
            va="bottom",
            fontsize=10,
            color="black",
        )

    ax1.legend(loc="upper left")
    plt.title(f"Expenses ({granularity.capitalize()}wise) per User with Total Expenses")
    plt.savefig("temp.png")
    plt.close()
    return open("temp.png", "rb")


def plot_single_user_expenses(df, userid, granularity="day", ndays=0):
    
    # Filter data for the specified user
    
    user_data = df[df["userid"] == userid]

    if user_data.empty:
        print(f"No data found for userid {userid}.")
        return

    fig, ax1 = plt.subplots(figsize=(12, 6))
    

    # Plot user expenses
    print(df)
    L = len(user_data["timestamp"])
    df = df.astype({'expense':'float'})
    total_expenses_per_day = df.groupby("timestamp")["expense"].sum().reset_index()
    print(total_expenses_per_day["expense"])
    if ndays == 0:
        ndays = L
    l = L - ndays
    ax1.plot(
        pd.to_datetime(total_expenses_per_day["timestamp"][l:]),
        total_expenses_per_day["expense"][l:],
        label=f"User {userid}",
        marker="o",
    )

    # Format x-axis
    ax1.xaxis.set_major_locator(
        mdates.DayLocator() if granularity == "day" else mdates.MonthLocator()
    )
    ax1.xaxis.set_major_formatter(
        mdates.DateFormatter("%Y-%m-%d" if granularity == "day" else "%Y-%m")
    )
    fig.autofmt_xdate()

    # Set labels and title
    ax1.set_xlabel(f"{granularity.capitalize()}s")
    ax1.set_ylabel("Expense Amount")
    plt.title(f"Expenses ({granularity.capitalize()}wise) for User {userid}")

    # Add legend and show plot
    ax1.legend(loc="upper left")
    plt.savefig("temp.png")
    plt.close()
    return open("temp.png", "rb")
