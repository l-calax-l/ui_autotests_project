import allure

from base.base_page import BasePage
from config.links import Links
from config.pydantic_config import settings


class SqlPage(BasePage):

    PAGE_PATH = Links.BASE_PAGE_2

    # --- Хедер ---
    LNK_USER = ("xpath", "//td[@align='right']//a[@href='/personal.php']")
    BTN_LOGOUT = ("xpath", "//a[@href='/logout.php']")

    # --- Поля ввода ---
    FLD_LOGIN = ("css selector", "input[name='login']")
    FLD_PASS = ("css selector", "input[type='password']")

    # --- Кнопка логин ---
    BTN_LOGIN = ("css selector", "input[value='Вход']")

    # --- Вкладки ---
    TAB_EXERCISE = ("css selector", "a[href=\"javascript:changeSt('exe')\"]")

    LNK_SELECT = ("css selector", "a[href='/learn_exercises.php']")

    LNK_LIST_EXERCISE = (
        "xpath",
        "//b[contains(text(),'Краткая информация о базе данных')]",
    )

    def perform_login(
        self, login: str = settings.login, password: str = settings.password
    ) -> None:
        with allure.step(f"Войти в аккаунт: {login}"):
            self.send_keys(self.FLD_LOGIN, login, "Логин")
            self.send_keys(self.FLD_PASS, password, "Пароль")
            self.click(self.BTN_LOGIN)
