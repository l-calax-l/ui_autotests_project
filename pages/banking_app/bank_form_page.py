import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

from base.base_page import BasePage
from config.links import Links


class BankFormPage(BasePage):

    PAGE_PATH = Links.BANK_FORM_PAGE

    # --- Основные поля ввода ---
    FLD_FIRST_NAME = ("id", "firstName")
    FLD_LAST_NAME = ("id", "lastName")
    FLD_EMAIL = ("id", "email")
    FLD_PASSWORD = ("id", "password")

    # --- Селекторы и чекбоксы ---
    # WARNING: Чекбоксы не имеют ID, выбираем через группу лейблов
    CHK_HOBBIES = ("xpath", "//div[@class='checkbox-group']/label")

    SEL_GENDER = ("id", "gender")
    AREA_ABOUT = ("id", "about")

    # --- Действия и Сообщения ---
    BTN_SUBMIT = ("css selector", "button[type='submit']")
    LBL_SUCCESS_MSG = ("id", "successMessage")

    def get_longest_hobby(self):
        with allure.step("Программное вычисление самого длинного хобби"):
            hobbies = self.find_elements(self.CHK_HOBBIES)
            return max(
                (hobby.text.strip() for hobby in hobbies if hobby.text.strip()), key=len
            )

    def select_hobby(self, target_hobby):
        hobbies = self.find_elements(self.CHK_HOBBIES)
        for hobby in hobbies:
            if target_hobby in hobby.text.strip():
                hobby.click()
                return
        raise AssertionError(f"Хобби '{target_hobby}' не найдено в списке!")

    def select_gender(self, target_gender):
        with allure.step(f"Выбрать пол из списка: {target_gender}"):
            select_element = self.find_element(
                self.SEL_GENDER, "выпадающий список Gender"
            )

            select = Select(select_element)

            select.select_by_visible_text(target_gender)

    def fill_registration_form(self, user_data, hobby=None, about=None, gender=None):
        with allure.step(f"Заполнить форму регистрации полностью"):
            self.send_keys(
                self.FLD_FIRST_NAME, user_data["first_name"], "поле firstname"
            )
            self.send_keys(self.FLD_LAST_NAME, user_data["last_name"], "поле lastname")
            self.send_keys(self.FLD_EMAIL, user_data["email"], "поле email")
            self.send_keys(self.FLD_PASSWORD, user_data["password"], "поле password")
            if hobby:
                self.select_hobby(hobby)
            if gender:
                self.select_gender(gender)

            if about:
                self.send_keys(
                    self.AREA_ABOUT,
                    f"Самое длинное слово из предложенных хобби - '{about}'",
                    "поле About Yourself",
                )

    def click_register(self):
        with allure.step("Кликнуть на кнопку 'Register'"):
            self.wait.until(EC.element_to_be_clickable(self.BTN_SUBMIT)).click()
