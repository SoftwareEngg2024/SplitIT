# About MyExpenseBot's /expense_graph Feature
This feature provides the user with their monthly and daily expense graphs for visualization. It also offers plotting your own graphs or the graphs of your group.

## Image processing Functions

### 1. `img_preprocess(img):`
This function preprocesses the image and prepares it to scan for OCR using pytesseract.



### 2. `img_process(img):`
This function processes the preprocessed image and returns a dict of scanned expenses.

#### Bot run Description

### 1. `run(message, bot):`
This is the initial trigger functipon of the module and is called after the bot receives ```/expense_graph``` as a message


### 2. `monthwise_or_daywise_record(message, bot):`
This function gets the input from user and decides to branch to plotting monthwise or daywise records.

### 3 `vis_graph_record(message, bot, granularity):`
This function gets the input of months/days that the user has inputted in reply to previous message.

### 4. `single_or_group_expenses(message, bot, granularity):`
This function gets the input from user to decide whether they want to plot their own or their group expenses

### 5. `plot_expenses_with_histogram(df, granularity="day", ndays=0):`
Main plotting function for group expense plotting.


### 6. `plot_single_user_expenses(df, granularity="day", ndays=0):`
Main plotting function for single expense plotting.

#### Description


## How to Run

1. Ensure that the required libraries are installed.
2. Execute the script to get the desired graph at desired granularity.

For detailed instructions on running the entire project, refer to the main README.md file.
