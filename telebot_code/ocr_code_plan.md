# OCR plan

Cycle:
1. User requests ocr 
2. prompt for photo
3. Once photo is received, validate
    If not photo, ask again
4. Send a copy of the interpreted ocr text.
    If not satisfactory provide option for manual input.
5. Ask if you want to add it as a single user expense or group expense 
6. Ask if you want to add it as a total expense or separate expenses.
7. Add expense.

# Testing
This will not be tested traditionally.
1. This will be included into release with manual testing. (No pytest)
2. The testing will involve taking direct user feedback from step 4. 
3. We will check the percentage of people who opt for manual insertions into the database.