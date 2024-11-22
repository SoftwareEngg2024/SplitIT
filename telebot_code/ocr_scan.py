import helper
import models
import telebot
from telebot import types
import add
import add_group_exp

import cv2
import pytesseract


def run(message, bot):

    if message.photo is None or len(message.photo)== 0:
        msg = bot.reply_to(message, "Sorry, there are no photos in the message you sent. Please try again.")
        bot.register_next_step_handler(msg, run, bot)
    elif len(message.photo) > 0:
        msg = bot.reply_to(message, "Sorry, Only a single photo can be processed at the moment. Please try again.")
        bot.register_next_step_handler(msg, run, bot)
    else:
        photo = message.photo[0]
        tempfilepath = bot.get_file(photo.file_id).path
        tempfile = bot.download_file(tempfilepath)
        img = cv2.imread(tempfilepath)
        exp = img_process(img_preprocess(img))
        
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Yes")
        markup.add("No")
        bot.reply_to(message, "This is the Scanned bill:\n"+print_exp(exp)+"\nAre you sure this is correct?", reply_markup=markup)
        bot.register_next_step_handler(msg, expense_type_selection_or_retry, bot, exp)

def expense_type_selection_or_retry(message, bot, exp):
    if message.text == "Yes":
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for expenseType in helper.getScannedExpenseOptions().values():
            markup.add(expenseType)
        
        msg = bot.reply_to(message, "Do you want this as a complete expense or a broken up expense?", reply_markup=markup)
        bot.register_next_step_handler(msg, post_scan_expense_type_selection, bot, exp)
    else:
        msg = bot.reply_to(message, "Sure, you can try again.")
        bot.register_next_step_handler(msg, run, bot)
            

def post_scan_expense_type_selection(message, bot, exp):
        if message.text == helper.getScannedExpenseOptions()["complete"]:
            expenseRecord = helper.ExpenseRecord(title="Expense", date=exp["date"], category="Expense", amount=exp["total"], currency=exp["currency"], amountUSD=0.0)
            add.add_user_expense_record(bot, message.from_user.id, expenseRecord.to_dict())
            
        elif message.text == helper.getScannedExpenseOptions()['brokenUp']:
            for eachexpense in exp["prices"]:
                expenseRecord = helper.ExpenseRecord(title="Expense", date=exp["date"], category="Expense", amount=eachexpense, currency=exp["currency"], amountUSD=0.0)
                add.add_user_expense_record(bot, message.from_user.id, expenseRecord.to_dict())

def print_exp(exp):
    strp = ""
    strp += "Date:\t"+exp["date"]
    for i in range(len(exp["items"])):
        strp += exp["items"][i]+":\t"+exp["currency"]+exp["prices"][i]+"\n"
    strp += "Total:\t"+exp["total"]
    return strp
        
def img_preprocess(img):
    return img

def img_process(img):
    return {"date":"", "currency":"USD", "items" : [], "prices" : [], "total" : 0.0 }
