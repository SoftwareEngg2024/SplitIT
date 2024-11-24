import imutils.perspective
import helper
import models
import telebot
from telebot import types
import add
import logging
import add_group_exp
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from telebot import types
from datetime import datetime, date, timedelta
from currency_api import update_currencies
from models import *
from db_operations import *
import cv2
import imutils
from thefuzz import fuzz
import re
import pytesseract
import requests
from code import api_token
def isfloat(num):
    return num.replace('.','',1).replace(",", "", 1).isdigit()


def run(message, bot):
    id = message.chat.id
    msg = bot.send_message(id, "Make sure that the letters are clearly legible. At the moment we offer the best support for Walmart receipts, however we are working on it!\nPlease provide a photo of your bill.")
    bot.register_next_step_handler(msg, photo_receive_handler, bot)

def download_file(bot, photo):
    tempfile = bot.get_file(photo.file_id)
    F = requests.get("https://api.telegram.org/file/bot"+str(api_token)+"/"+tempfile.file_path)
    fname = tempfile.file_path.split("/")[-1]
    with open(fname, "wb") as fp:
        fp.write(F.content)
    return fname

def photo_receive_handler(message, bot):
    id = message.chat.id
    if message.photo is None or len(message.photo)== 0:
        msg = bot.reply_to(message, "Sorry, there are no photos in the message you sent. Please try again.")
        bot.register_next_step_handler(msg, photo_receive_handler, bot)
    elif len(message.photo) > 0:
        bot.send_message(id, "Only the first photo will be processed at the time.")
        photo = message.photo[-1]
        
        tempf = download_file(bot, photo)
        img = cv2.imread(tempf)
        exp = img_process(img_preprocess(img))
        if exp["invalid"] == 1:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("Yes")
            markup.add("No")
            msg = bot.reply_to(message, "The amounts were not correctly detected, or you might not have a compatible bill format. Do you want to enter manually?", reply_markup=markup)
            bot.register_next_step_handler(msg, post_auto_or_manual_selection, bot)
        else:   
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("Yes")
            markup.add("No")
            msg = bot.reply_to(message, "These are the amounts on the Scanned bill:\n"+print_exp(exp)+"\nAre you sure this is correct?", reply_markup=markup)
            bot.register_next_step_handler(msg, expense_type_selection_or_retry, bot, exp)

def expense_type_selection_or_retry(message, bot, exp):
    if message.text == "Yes":
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for expenseType in helper.getScannedExpenseOptions().values():
            markup.add(expenseType)
        
        msg = bot.reply_to(message, "Do you want this as a complete expense or a broken up expense?", reply_markup=markup)
        bot.register_next_step_handler(msg, post_scan_expense_type_selection, bot, exp)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Yes")
        markup.add("No")
        msg = bot.reply_to(message, "Do you want to enter manually?", reply_markup=markup)
        bot.register_next_step_handler(msg, post_auto_or_manual_selection, bot)


def post_date_choice_input(message, bot, amounts):
    try:
        if message.text == "Today":
            post_date_input(message, bot, amounts, date.today())
        else:
            chat_id = message.chat.id
            user_id = message.from_user.id
            calendar, step = DetailedTelegramCalendar().build()
            bot.send_message(chat_id, f"Select {LSTEP[step]}", reply_markup=calendar)
            
        
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
                    post_date_input(message,bot, result)
                    bot.edit_message_text(
                        f"Date is set: {result}",
                        c.message.chat.id,
                        c.message.message_id,
                    )
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, 'Oh no. ' + str(e))

def post_date_input(message, bot, amounts, date_entered):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        amount = amounts
        currency = "USD"

        ####################################################

        formatted_date = date_entered.strftime('%Y-%m-%d')
        date_object = datetime.strptime(formatted_date, '%Y-%m-%d')
        start_date = datetime.strptime('1999-01-01', '%Y-%m-%d')
        end_date = datetime.today() + + timedelta(days=7)

        # Check if the date falls within the range
        if start_date <= date_object <= end_date:
            for amt in amounts:
                amountval = add.actual_curr_val(currency, amt, formatted_date)
                expenseRecord = ExpenseRecord(title="Expense", date=formatted_date, category="Bill", amount=amt, currency="USD", amountUSD=amountval)
                
                add.add_user_income_record(bot,user_id, expenseRecord.to_dict())
            bot.send_message(chat_id, 'The expenditure has been recorded.')
            
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("Custom")
            markup.add("Today")
            
            msg = bot.reply_to(message, "Try again. Do you want to enter today's date or a custom date?", reply_markup=markup)
            bot.register_next_step_handler(msg, post_date_choice_input, bot)

        # if currency == 'Euro':
        #     actual_value = float(amount) * 1.05
        # elif currency == 'INR':
        #     actual_value = float(amount) * 0.012
        # else:
        #     actual_value = float(amount) * 1.0
        # amountval = round(actual_value, 2)

        ######################################################
        

    ####################################################
    except Exception as e:
        error_message = f'Oh no. An error occurred:\n{e}'
        bot.reply_to(message, error_message)
        logging.exception(str(e))
    ####################################################

def post_auto_or_manual_selection(message, bot):
    if message.text == "No":
        msg = bot.reply_to(message, "Sure, you can try again.")
        bot.register_next_step_handler(msg, run, bot)
    else:
        bot.send_message("OK. Enter your expense date.")
        bot.register_next_step_handler(msg, post_manual_expense_selection, bot, [])

def post_manual_expense_selection(message, bot):
    T = message.text
    expenses = T.split(",")
    incorr = 0
    p_expenses = []
    for exp in expenses:
        amt = helper.validate_entered_amount(exp)
        if amt == 0:
            incorr = 1
            break
        else:
            p_expenses.append(amt)
    if incorr == 1:
        msg = bot.reply_to("OK. Enter your expenses in a comma-separated fashion:")
        bot.register_next_step_handler(msg, post_manual_expense_selection, bot, [])
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Custom")
        markup.add("Today")
        msg = bot.reply_to("Choose your desired date", reply_markup=markup)
        bot.register_next_step_handler(msg, post_date_choice_input, bot, p_expenses)


def post_scan_expense_type_selection(message, bot, exp):
        exp["date"] = date.today().strftime("%Y-%m-%d")
        if message.text == helper.getScannedExpenseOptions()["complete"]:
            expenseRecord = helper.ExpenseRecord(title="Expense", date=exp["date"], category="Expense", amount=exp["total"], currency=exp["currency"], amountUSD=0.0)
            add.add_user_expense_record(bot, message.from_user.id, expenseRecord.to_dict())
            
        elif message.text == helper.getScannedExpenseOptions()['brokenUp']:
            for eachexpense in exp["prices"]:
                expenseRecord = helper.ExpenseRecord(title="Expense", date=exp["date"], category="Expense", amount=eachexpense, currency=exp["currency"], amountUSD=0.0)
                add.add_user_expense_record(bot, message.from_user.id, expenseRecord.to_dict())

def print_exp(exp):
    strp = ""
    for i in range(len(exp["prices"])):
        strp += exp["currency"]+exp["prices"][i]+"\n"
    if "total" in exp.keys():
        strp += "Total:\t"+exp["total"]
    return strp
        
def img_preprocess(img):
    image = img.copy()
    if image.shape[0] < 800:
        image = imutils.resize(image, width=800)
    ratio = img.shape[1] / float(image.shape[1])
    area = image.shape[0] * image.shape[1]

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3,3,),0,)
    edged = cv2.Canny(blurred, 65, 180)

    contours = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)


    receipt_contour = None

    for c in contours:
        
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        
        if len(approx) == 4:
            receipt_contour = approx
            break

    # cv2.drawContours(image, [receipt_contour], -1, (0, 255, 0), 2)
    # # cv2.imwrite('image_with_outline.jpg', image)
    # cv2.imshow("Receipt Outline", image)
    # cv2.waitKey(0)
    if receipt_contour is None:
        receipt = blurred
    else:
        receipt = imutils.perspective.four_point_transform(img, receipt_contour.reshape(4, 2) * ratio)

    receipt = cv2.cvtColor(receipt, cv2.COLOR_BGR2GRAY)
    if (cv2.contourArea(receipt_contour)/area < 0.30):
        receipt = blurred
    g = cv2.threshold(receipt, 0, 255, cv2.THRESH_OTSU)[0]
    g2 = cv2.threshold(receipt, g * 0.9, 255, cv2.THRESH_BINARY)[1]
    return g2


def img_process(img):
    options = "--psm 6"
    text = pytesseract.image_to_string(
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB), lang='eng', config=options
    )
    # show the raw output of the OCR process
    print("[INFO] raw output:")
    print("==================")
    print(text)
    print("\n")
    sn = text.split("\n")
    dictp = {}
    taxcalc = 0
    dictp["invalid"] = 0
    dictp["prices"] = []
    for line in sn:
        P = line.split()
        total_ratio = fuzz.partial_ratio(line, "TOTAL")
        subtotal_ratio = fuzz.partial_ratio(line, "SUBTOTAL")
        tax_ratio = fuzz.partial_ratio(line, "TAX")
        
        print(line)
        print(total_ratio)
        print(subtotal_ratio)
        print(tax_ratio)
        if subtotal_ratio > 80 and total_ratio <= subtotal_ratio:
            s = re.findall(r"[$]?\d+[ ]*[,.][ ]*\d+", line)
            if (len(s) == 0):
                dictp["subtotal"] = "-1.0"
            else:
                dictp["subtotal"] = s[0].strip().replace(" ","").replace(",", ".").replace("$", "")
        elif tax_ratio > 70.0:
            continue
        elif total_ratio > 80 and total_ratio >= subtotal_ratio:
            s = re.findall(r"[$]?\d+[ ]*[,.][ ]*\d+", line)
            print(s)
            if (len(s) == 0):
                dictp["total"] = "-1.0"
            else:
                dictp["total"] = s[0].strip().replace(" ","").replace(",", ".").replace("$", "")
            break
        else:
            s = re.findall(r"[$]?\d+[ ]*[,.][ ]*\d+", line)
            if len(s) == 0 or "TAX" in line:
                continue
            dictp["prices"].append(s[0].strip().replace(" ","").replace(",", ".").replace("$", ""))
            pass
    dictp["currency"] = "USD"
    if "total" in dictp.keys() and "subtotal" in dictp.keys():
        if isfloat(dictp["total"]) and isfloat(dictp["subtotal"]):
            dictp["tax"] = str(round(float(dictp["total"]) - float(dictp["subtotal"]), 2))
        else:

            dictp["invalid"] = 1
            
            print("Invalid scan. Try again.")
    elif len(dictp["prices"]) == 0:
        dictp["invalid"] = 1
    return dictp
