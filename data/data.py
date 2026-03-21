from faker import Faker

fake = Faker()


class RegPageData:
    VALID = {"username": "angular", "password": "password"}
    INVALID = {"username": "wrong_user", "password": "wrong_password"}


class BankLoginData:
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    password = fake.password()

    VALID = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
    }

    INVALID = {"firstname": " ", "lastname": " ", "email": " ", "password": " "}


class ManagerPageData:
    first_name = fake.first_name()
    last_name = fake.last_name()
    post_code = fake.postcode()

    VALID = {
        "first_name": first_name,
        "last_name": last_name,
        "post_code": post_code,
    }
