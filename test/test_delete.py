import os
import json
from telebot_code import delete
from unittest.mock import patch, MagicMock
from telebot import types
import pytest

# Mock helper function to create a fake Message object
def create_mock_message(text, chat_id=1, user_id=1, message_id=1):
    message = MagicMock(spec=types.Message)
    message.message_id = message_id
    message.text = text
    message.chat = MagicMock(id=chat_id, type="private")
    message.from_user = MagicMock(id=user_id, is_bot=False, first_name="TestUser")
    return message

# Helper function to simulate reading JSON data
def test_read_json():
    try:
        if not os.path.exists('./test/dummy_expense_record.json'):
            with open('./test/dummy_expense_record.json', 'w') as json_file:
                json_file.write('{}')
            return json.loads('{}')
        elif os.stat('./test/dummy_expense_record.json').st_size != 0:
            with open('./test/dummy_expense_record.json') as expense_record:
                expense_record_data = json.load(expense_record)
            return expense_record_data
    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")
        return {}

# @patch('telebot.TeleBot')
# def test_delete_run_with_data(mock_telebot, mocker):
#     # Mock helper and database operations
#     mocker.patch.object(delete.helper, 'read_json', return_value={"user_id": 1, "transactions": ["expense1"]})
#     mocker.patch.object(delete.helper, 'write_json', return_value=True)
#     mocker.patch('db_operations.read_user_transaction', return_value={"transactions": ["expense1"]})
#     mocker.patch('db_operations.delete_user_transaction', return_value=True)

#     # Mock message and bot
#     MOCK_Message_data = create_mock_message("Delete expenses")
#     mock_bot_instance = mock_telebot.return_value
#     mock_bot_instance.send_message.return_value = True

#     # Run the delete function
#     delete.run(MOCK_Message_data, mock_bot_instance)

#     # Add assertions to check if the data is processed correctly
#     # Check if read_json is called correctly
#     delete.helper.read_json.assert_called_once()
    
#     # Assert that write_json was called
#     assert delete.helper.write_json.called, "write_json was not called!"
    
#     # Ensure the send_message was called with the correct message
#     mock_bot_instance.send_message.assert_called_once_with(
#         MOCK_Message_data.chat.id, "Your records have been deleted successfully!"
#     )



@patch('telebot.TeleBot')
def test_delete_with_no_data(mock_telebot, mocker):
    # Mock helper and database operations
    mocker.patch.object(delete.helper, 'read_json', return_value={})
    mocker.patch.object(delete.helper, 'write_json', return_value=True)
    mocker.patch('db_operations.read_user_transaction', return_value=None)
    mocker.patch('db_operations.delete_user_transaction', return_value=None)

    # Mock message and bot
    MOCK_Message_data = create_mock_message("Delete expenses")
    mock_bot_instance = mock_telebot.return_value
    mock_bot_instance.send_message.return_value = True

    # Run the delete function
    delete.run(MOCK_Message_data, mock_bot_instance)

    # Assert that send_message is called with correct text
    mock_bot_instance.send_message.assert_called_once_with(MOCK_Message_data.chat.id, "No records there to be deleted. Start adding your expenses to keep track of your spendings!")
