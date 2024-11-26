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
1. Open user.properties in your project.
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
