# About MyExpenseBot's `/ocr_scan` Feature

The `scan` feature in SplitIT enables the telegram bot to receive photos of receipts and scan them for expenses.

## Image processing Functions

### 1. `img_preprocess(img):`
This function preprocesses the image and prepares it to scan for OCR using pytesseract.



### 2. `img_process(img):`
This function processes the preprocessed image and returns a dict of scanned expenses.

#### Bot run Description

### 3. `run(message, bot):`
This is the initial trigger functipon of the module and is called after the bot receives ```/scan``` as a message

### 4. `download_file(bot, photo):`
This function downloads the photo file provided onto the storage for the bot on the telegram servers, once the user has sent their photo.

### 5. `photo_receive_handler(message, bot):`
This function handles the reception of the photo from the user to the bot backend, via telegram servers. It also generates the ocr text on reception and sends it to the user.

### 5. `post_auto_or_manual_selection(message, bot):`
This function provides the user to input the expenses manually, should the correct amounts not be detected by the OCR.

### 6. `post_manual_expense_selection(message, bot):`
This function receives the user expenses in comma separated values and adds the espenses to the database.

#### Description


## How to Run

1. Ensure that the required libraries are installed.
2. Execute the script to scan the provided receipts and get the text through OCR method.
3. Add the expenses or choose to insert manually.

For detailed instructions on running the entire project, refer to the main README.md file.
