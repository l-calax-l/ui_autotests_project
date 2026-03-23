import allure
from selenium.webdriver.support import expected_conditions as EC

from base.base_page import BasePage
from config.links import Links


class RegPage(BasePage):

    PAGE_PATH = Links.REG_PAGE

    # --- Поля ввода ---
    FLD_USERNAME = ("id", "username")
    FLD_PASSWORD = ("id", "password")
    LBL_USER_DESCRIPTION = ("css selector", "[ng-model='model[options.key]']")

    # --- Кнопки управления ---
    BTN_LOGIN = ("css selector", "button.btn-danger")
    LNK_LOGOUT = ("css selector", 'a[href="#/login"]')

    # --- Состояния и Фидбек ---
    IMG_LOADING = ("css selector", "img[ng-if*='Load']")

    LBL_SUCCESS_MSG = ("xpath", "//p[1]")
    LBL_ERROR_MSG = ("css selector", ".alert-danger")

    def enter_reg_data(self, data):
        with allure.step(f"Заполнить данные username и password"):
            self.send_keys(self.FLD_USERNAME, data["username"], "username")
            self.send_keys(self.FLD_PASSWORD, data["password"], "password")
            self.send_keys(
                self.LBL_USER_DESCRIPTION, data["username"], "username* description"
            )

    def wait_until_invisible(self, locator, locator_name=None):
        with allure.step(f"Ждем пока элемент '{locator_name or locator}' не исчезнет"):
            self.wait.until(EC.invisibility_of_element_located(locator))
