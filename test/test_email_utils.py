# import unittest
# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'telebot_code')))
# from telebot_code.email_utils import send_email

# class TestEmailUtils(unittest.TestCase):

#     def test_send_email_does_not_raise_error(self):
#         # Check if send_email doesn't raise an error when called
#         try:
#             send_email("test@example.com", "Subject", "Body")
#             result = True
#         except:
#             result = False
#         self.assertTrue(result, "send_email should not raise any error.")

#     def test_send_email_with_empty_recipient(self):
#         # Check if send_email with empty recipient raises an error
#         with self.assertRaises(Exception):
#             send_email("", "Subject", "Body")

#     def test_send_email_with_empty_subject(self):
#         # Check if send_email with empty subject raises an error
#         with self.assertRaises(Exception):
#             send_email("test@example.com", "", "Body")

#     def test_send_email_with_empty_body(self):
#         # Check if send_email with empty body raises an error
#         with self.assertRaises(Exception):
#             send_email("test@example.com", "Subject", "")

#     def test_send_email_with_valid_data(self):
#         # Just check if send_email works with simple valid data
#         try:
#             send_email("test@example.com", "Test Subject", "Test Body")
#             result = True
#         except:
#             result = False
#         self.assertTrue(result, "send_email with valid data should not raise an error.")

#     def test_email_subject_is_string(self):
#     # Stupid but relatable test: Check if the subject of the email is a string
#         subject = "Test Subject"
#         self.assertIsInstance(subject, str)  # This will always pass as 'subject' is always a string


# if __name__ == "__main__":
#     unittest.main()
import pytest
from telebot_code.email_utils import send_email


def test_send_email_does_not_raise_error():
    # Check if send_email doesn't raise an error when called
    try:
        send_email("test@example.com", "Subject", "Body")
    except Exception as e:
        pytest.fail(f"send_email raised an unexpected exception: {e}")


def test_send_email_with_empty_recipient():
    # Check if send_email with empty recipient raises an error
    with pytest.raises(Exception):
        send_email("", "Subject", "Body")


def test_send_email_with_empty_subject():
    # Check if send_email with empty subject raises an error
    with pytest.raises(Exception):
        send_email("test@example.com", "", "Body")


def test_send_email_with_empty_body():
    # Check if send_email with empty body raises an error
    with pytest.raises(Exception):
        send_email("test@example.com", "Subject", "")


def test_send_email_with_valid_data():
    # Check if send_email works with simple valid data
    try:
        send_email("test@example.com", "Test Subject", "Test Body")
    except Exception as e:
        pytest.fail(f"send_email raised an unexpected exception: {e}")


# Stupid but relatable test case
def test_email_subject_is_string():
    subject = "Test Subject"
    assert isinstance(subject, str), "Email subject should be a string"