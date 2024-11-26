import helper
import logging
from telebot import types
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def run(message, bot):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    options = helper.getIncomeOrExpense()
    markup.row_width = 2
    for c in options.values():
        markup.add(c)
    msg = bot.reply_to(message, "Select Income or Expense", reply_markup=markup)
    bot.register_next_step_handler(msg, post_type_selection, bot)


def post_type_selection(message, bot):
    try:
        chat_id = message.chat.id
        selectedType = message.text
        user_history = helper.getUserHistory(chat_id, selectedType)
        nrecs = len(user_history)
        
        print(nrecs)
        print(user_history)
        if len(user_history) == 0:
                plt.text(
                    0.1,
                    top,
                    "No record found!",
                    horizontalalignment="left",
                    verticalalignment="center",
                    transform=ax.transAxes,
                    fontsize=20,
                )
        else:
            recsperpage = 6
            npages = int(nrecs/recsperpage) + 1
            message = "Alright. I just created a pdf of your " + selectedType + "history!"
            bot.send_message(chat_id, message)
            with PdfPages("user_history.pdf") as pdf:
                if len(user_history) == 0:
                    plt.text(
                        0.1,
                        top,
                        "No record found!",
                        horizontalalignment="left",
                        verticalalignment="center",
                        transform=ax.transAxes,
                        fontsize=20,
                    )
                else:

                    for i in range(npages):
                        fig = plt.figure()
                        ax = fig.add_subplot(1, 1, 1)
                        top = 0.8
                        
                        for j in range(i * recsperpage, min(nrecs, (i + 1) * (recsperpage))):
                            rec = user_history[j]
                            date = rec['date']
                            category = rec['category']
                            amount = rec['amount']
                            curr = rec['currency']
                            actualVal = rec['amountUSD']
                            print(date, category, amount)
                            if selectedType == "Income":
                                rec_str = f"{amount}$ {category} income on {date} -- Actual Value entered is {curr} {actualVal}"
                            else:
                                rec_str = f"{amount}$ {category} expense on {date} -- Actual Value entered is {curr} {actualVal}"
                            plt.text(
                                0,
                                top,
                                rec_str,
                                horizontalalignment="left",
                                verticalalignment="center",
                                transform=ax.transAxes,
                                fontsize=10,
                                bbox=dict(facecolor="red", alpha=0.3),
                            )
                            top -= 0.15
                        plt.axis("off")
                        pdf.savefig()
                        plt.close()
        bot.send_document(chat_id, open("user_history.pdf", "rb"))
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oops!" + str(e))
