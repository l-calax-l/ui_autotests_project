from faker import Faker
from data.excel_reader import ExcelDataReader

fake = Faker()
reader = ExcelDataReader()


class RegPageData:
    VALID_LIST = reader.get_reg_page_valid()
    INVALID_LIST = reader.get_reg_page_invalid()

    VALID = VALID_LIST[0] if VALID_LIST else {"username": "angular", "password": "password"}
    INVALID = INVALID_LIST[0] if INVALID_LIST else {"username": "wrong_user", "password": "wrong_password"}


class BankLoginData:
    VALID_LIST = reader.get_bank_login_valid()
    INVALID_LIST = reader.get_bank_login_invalid()

    VALID = VALID_LIST[0] if VALID_LIST else {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "password": fake.password(),
    }
    INVALID = INVALID_LIST[0] if INVALID_LIST else {
        "first_name": " ",
        "last_name": " ",
        "email": " ",
        "password": " ",
    }


class ManagerPageData:
    VALID_LIST = reader.get_manager_valid()
    INVALID_LIST = reader.get_manager_invalid()

    VALID = VALID_LIST[0] if VALID_LIST else {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "post_code": fake.postcode(),
    }