import allure

from base.base_page import BasePage
from config.links import Links
from config.pydantic_config import settings
from utils.logger import get_logger

logger = get_logger(__name__)


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

    FLD_CODE_EXERCISE = ("css selector", "textarea[id='txtsql']")

    def perform_login(
        self, login: str = settings.login, password: str = settings.password
    ) -> None:
        with allure.step(f"Войти в аккаунт: {login}"):
            logger.info(f"Логин в аккаунт, пользователь: {login}")
            self.send_keys(self.FLD_LOGIN, login, "Логин")
            self.send_keys(self.FLD_PASS, password, "Пароль")
            self.click(self.BTN_LOGIN)
            logger.info(
                f"Кнопка логина нажата, запрос на авторизацию отправлен для: {login}"
            )

    def move_to_exercise(self) -> None:
        with allure.step("Перейти на вкладку с SQL задачами"):
            self.click(self.TAB_EXERCISE, "Упражнения по SQL")
            self.click(self.LNK_SELECT, "SELECT (обучающий этап)")
