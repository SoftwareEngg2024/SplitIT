# 💰 TrackMyDollar V3.0 - MyExpenseBot 💰

Link to Demo of Phase 4 - https://www.youtube.com/watch?v=Q4XcCcaFqmo

MyExpenseBot shows the features added to the exisiting TrackMyDollar to improve scalability.
<hr>
<p align="center">
<a><img  height=360 width=550 
  src="https://github.com/nainisha-b/MyExpenseBot/blob/main/docs/Tracking_income_and_expenses.png" alt="Income and Expense tracking made easy!"></a>
</p>
<hr>

![MIT license](https://img.shields.io/badge/License-MIT-green.svg)
[![Platform](https://img.shields.io/badge/Platform-Telegram-blue)](https://desktop.telegram.org/)
![GitHub](https://img.shields.io/badge/Language-Python-blue.svg)
[![GitHub contributors](https://img.shields.io/github/contributors/nainisha-b/MyExpenseBot)](https://github.com/nainisha-b/MyExpenseBot/graphs/contributors)
[![DOI](https://zenodo.org/badge/414661894.svg)](https://zenodo.org/badge/latestdoi/414661894)
[![Build Status](https://app.travis-ci.com/sak007/MyDollarBot-BOTGo.svg?branch=main)](https://app.travis-ci.com/github/sak007/MyDollarBot-BOTGo)
[![codecov](https://codecov.io/gh/sak007/MyDollarBot-BOTGo/branch/main/graph/badge.svg?token=5AYMR8MNMP)](https://codecov.io/gh/sak007/MyDollarBot-BOTGo)
[![GitHub issues](https://img.shields.io/github/issues/nainisha-b/MyExpenseBot)](https://github.com/nainisha-b/MyExpenseBot/issues?q=is%3Aopen+is%3Aissue)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/nainisha-b/MyExpenseBot)](https://github.com/nainisha-b/MyExpenseBot/issues?q=is%3Aissue+is%3Aclosed)

![Fork](https://img.shields.io/github/forks/nainisha-b/MyExpenseBot?style=social)
<hr>

## About MyExpenseBot(Based on Phase 2, 3 and Phase 4)

MyExpenseBot is an easy-to-use Telegram Bot that assists you in recording your daily expenses on a local system without any hassle 
With simple commands, this bot allows you to:
- Add/Record a new spending
- Show the sum of your expenditure for the current day/month
- Display your spending history
- Clear/Erase all your records
- Edit/Change any spending details if you wish to
- Recurring expense:
  Add a recurring expense that adds a certain amount every month to the user's spending, for any given category.
- Custom category:
  User can add a new category and delete an existing category as per the needs
- Budgeting:
  User can see the budget value for the total expense and/or for each of the existing categories in the /display function
- Better visualization:
  Added pie charts, bar graphs with and without budget lines for the user to have a look at the spending history in a better manner
  Added bar graph in the /history command to see spending across different categories
  User can see the daily and monthly expenses for spending history.
- Deployment on GCP (the bot is now available, and can be used on any device by searching for @testforbudgetmanagerbot on Telegram) 

## What's new? (From Phase 4 to Phase 5)
The new design of the Telegram Bot resolves the issues of the Phase 3
- Incorporated 17 more currencies into the Telegram Expense Bot using [Currency API](https://www.currencyapi.com).
- Implemented Local JSON Caching to reduce API calls for currency values.
- Added the feature which stops taking the future date input for income and expenditure.


## What's new? (From Phase 4 to Phase 5)
The new design of the Telegram Bot resolves the issues of the Phase 3
- Incorporated 17 more currencies into the Telegram Expense Bot using Currency API.
- Implemented Local JSON Caching to reduce API calls for currency values.
- Added the feature which stops taking the future date input for income and expenditure.


## What more can be done?
Please refer to the issue list available [here](https://github.com/orgs/NCSU-Group70-CSC505-SE-Fall-23/projects/1/views/1) to see what more can be done to make MyExpenseBot better. Please refer to the MyExpense project present [here](https://github.com/users/nainisha-b/projects/1) to have a look at the tasks to be done, tasks currently in progress and tasks already done.


## Demo

https://www.youtube.com/watch?v=BCTuqfJO7S0

## Installation guide

The below instructions can be followed in order to set-up this bot at your end in a span of few minutes! Let's get started:

1. Clone this repository to your local system.

2. Start a terminal session in the directory where the project has been cloned. Run the following command to install the required dependencies:
```
  pip install -r requirements.txt
```

3. Include the file path for "currencies.json" (which is situated in the main directory) within the add.py file (found in the main directory under the code subdirectory). In the add.py file, locate the "actual_curr_value" function. Refer to the image below.

   <img width="512" alt="image" src="https://github.com/NCSU-Group70-CSC505-SE-Fall-23/MyExpenseBot/assets/70905787/43ea13cb-b141-4ca1-a806-8f6d3354fdb6">


3. In Telegram, search for "BotFather". Click on "Start", and enter the following command:
```
  /newbot
```
Follow the instructions on screen and choose a name for your bot. After this, select a username for your bot that ends with "bot".

4. BotFather will now confirm the creation of your bot and provide a TOKEN to access the HTTP API - copy and save this token for future use and update this token in the user.properties file to connect this project to the telegram bot.

5. In the directory where this repo has been cloned, please run the below command to execute a bash script to run the Telegram Bot:
```
   ./run.sh
```
(OR)
```
   bash run.sh
```
Please note that it will ask you to paste the API token you received from Telegram in step 4.
A successful run will generate a message on your terminal that says "TeleBot: Started polling." 

6. In the Telegram app, search for your newly created bot by entering the username and open the same. Now, on Telegram, enter the "/start" or "/menu" command, and you are all set to track your expenses!

## Testing

We use pytest to perform testing on all unit tests together. The command needs to be run from the home directory of the project. The command is:
```
python -m pytest test/
```

## Code Coverage

Code coverage is part of the build. Every time new code is pushed to the repository, the build is run, and along with it, code coverage is computed. This can be viewed by selecting the build, and then choosing the codecov pop-up on hover.

Locally, we use the coverage package in python for code coverage. The commands to check code coverage in python are as follows:

```
coverage run -m pytest test/
coverage report
```

## Notes:
You can download and install the Telegram desktop application for your system from the following site: https://desktop.telegram.org/


<hr>
<p>Title:'Track My Income and Expense'</p>
<p>Version: '5.1'</p>
<p>Description: 'An easy to use Telegram Bot to track everyday income and expenses'</p>
<p>Authors(Iteration 5):'Nisarg, Chaitanya, Mitesh, Aniruddha'</p>
<p>Authors(Iteration 4):'Anvitha, Nainisha, Vaishnavi'</p>
<p>Authors(Iteration 3):'Vraj, Alex, Leo, Prithvish, Seeya'</p>
<p>Authors(Iteration 2):'Athithya, Subramanian, Ashok, Zunaid, Rithik'</p>
<p>Authors(Iteration 1):'Dev, Prakruthi, Radhika, Rohan, Sunidhi'</p>
