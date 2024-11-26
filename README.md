# CSC 510 Fall '24 - Group 41

# PocketTrack 💰📊  
<p align='center'>
<img alt="License: MIT" src="https://img.shields.io/badge/Lang-Python-green" />
<img alt="License: MIT" src="https://img.shields.io/badge/Code_Formatter-black-green" />
<a href='https://coveralls.io/github/SoftwareEngg2024/SplitIT?branch=release/1.1'><img src='https://coveralls.io/repos/github/SoftwareEngg2024/SplitIT/badge.svg?branch=release/1.1' alt='Coverage Status' /></a>
<a href="https://github.com/SoftwareEngg2024/SplitIT/actions/workflows/test_and_coverage.yaml"><img src='https://github.com/SoftwareEngg2024/SplitIT/actions/workflows/test_and_coverage.yaml/badge.svg?branch=release%2F1.1' /></a>
<a href="https://github.com/SoftwareEngg2024/SplitIT/tree/release/1.0/docs"><img alt="Documentation Status" src="https://img.shields.io/badge/Docs-Click-green"></a>
<img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green" />
 
</p>


## A telegram bot for tracking expenses 
**PocketTrack** is a smart and interactive Telegram bot that helps you manage your expenses with ease. Whether you’re tracking daily spending, analyzing monthly trends, or keeping your budget in check, PocketTrack is your go-to financial assistant.  

With new and enhanced features, PocketTrack simplifies expense management, offering a seamless and efficient user experience.  

---

## 🌟 New Features 🌟  

### 📧 Email Summaries  
Receive a detailed monthly expenditure report directly in your inbox! PocketTrack ensures you always stay informed about where your money is going, with clean, concise email updates.

### 📸 OCR Scan  
Save time with automated data entry! Use the OCR scan feature to extract expense details from receipts or bills, eliminating the need for manual input.  

### 📊 Expense Graphs  
 Visualize your spending habits! The new graph feature offers clear, interactive charts to help you analyze your expenses by category, day, or month, empowering you to make smarter financial decisions.  

### 📄 PDF Download  
Easily download your monthly expense reports in PDF format. Share or save your financial summaries for future reference with just one click.  

---

## 🚀 Future Scope  

### 📌 Shared Budget Management  
Collaborate with friends or family to manage shared budgets, track group expenses, and split costs effortlessly. This feature is ideal for roommates, travel groups, or anyone managing expenses as a team

### 📊 Predictive Expense Analysis  
Leverage AI to predict future spending trends based on your habits. This feature can alert you to potential overspending, recommend savings opportunities, and help you prepare for upcoming expenses.

### 💡 Gamification of Savings  
Turn saving money into a fun and rewarding experience! Earn badges for achieving savings milestones, streak rewards for consistent financial tracking, and personalized challenges to help you cut unnecessary spending.

### 🎉 Personalized Recommendations  
PocketTrack could provide tailored financial tips, such as spending advice, budgeting strategies, and savings plans based on your unique financial data and patterns.

### 📤 Automated Bill Reminders: 
Never miss a payment again! PocketTrack could notify you of upcoming bills, calculate the impact on your budget, and even send reminders directly to your Telegram account.

## Why PocketTrack?  
PocketTrack offers a user-friendly and robust experience that integrates directly into your daily life through Telegram. Whether you need to track expenses, analyze spending trends, or stay updated with email reports, PocketTrack simplifies the process, giving you the financial clarity you need.

Start your journey towards smarter financial management with PocketTrack! 🚀 


## 💻 Tech Stack

| Technology      | Icon                                                                                                     | Description                                                                                  |
|------------------|---------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| **MongoDB**      | ![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b?style=for-the-badge&logo=mongodb&logoColor=white) | A NoSQL database used for efficient and scalable data storage.                               |
| **Flask**        | ![Flask](https://img.shields.io/badge/Flask-%23000000?style=for-the-badge&logo=flask&logoColor=white)      | A lightweight web framework for building APIs and web applications in Python.               |
| **Python**       | ![Python](https://img.shields.io/badge/Python-%233776AB?style=for-the-badge&logo=python&logoColor=white)   | The core programming language used to develop the project.                                   |
| **Telegram API** | ![Telegram](https://img.shields.io/badge/Telegram-%2326A5E4?style=for-the-badge&logo=telegram&logoColor=white) | An API used to create and manage Telegram bot functionalities.                               |
| **OpenCV**       | ![OpenCV](https://img.shields.io/badge/OpenCV-%235C3EE8?style=for-the-badge&logo=opencv&logoColor=white)   | A computer vision library for image processing and analysis.                                 |
| **Tesseract**    | ![Tesseract](https://img.shields.io/badge/Tesseract-%232BB671?style=for-the-badge&logo=tesseract&logoColor=white) | An OCR engine used for text recognition in images.                                           |

## Installation Guide  

The below instructions can be followed in order to set up this bot at your end in just a few minutes!  

### Clone this Repository  
```bash
git clone git@github.com:SoftwareEngg2024/SplitIT.git
```
### Install Dependencies
Start a terminal session in the directory where the project has been cloned. Run the following command to install the required dependencies:
```bash
pip install -r requirements.txt
```
### Create Your Telegram Bot
1. Search for BotFather in Telegram.
2. Use /newbot to create a new bot.
3. Follow instructions and get a TOKEN.

### Create MongoDB Instance on MongoDB Atlas
1. Go to MongoDB Atlas, create a database.
2. Install MongoDB Compass.
3. Use the connection string from Atlas to connect to DB.
   
### Update TOKEN in user.properties
1. Open or create user.properties in your project.
2. Update the TOKEN and MONGODB_URI with your credentials.

### Run the Telegram Bot
Run the following command to start the bot:
```bash
./run.sh  (or) bash run.sh  (or) sh run.sh
```
Paste the Telegram API Token when prompted.
A successful run will display:
```bash
TeleBot: Started polling.
```

## Documentation 
Refer here [Wiki Page](https://github.com/SoftwareEngg2024/SplitIT/wiki/Delta-file-(New-Changes-since-last-version))

## Bug
Raise an issue on this repository, we would love to look at it!

## License 📃
This project is under MIT License.
- The MIT license explicitly grants users the right to reuse code for various purposes,hence for improval of future scope of the code we have added MIT license.
- They include the original MIT license when distributing it. Allowing users to customize or adapt the code to meet their specific requirements.


---  
```
