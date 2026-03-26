import allure
import pytest
from base.base_test import BaseTest

@pytest.mark.regression
@allure.epic("Демонстрация инфраструктуры")
@allure.feature("Тестирование механизма перезапуска (Rerun Failures)")
class TestFail(BaseTest):
    """
    Тестовый класс для проверки автоматического перезапуска падающих тестов (Задача U8).
    Эти тесты намеренно падают.
    """

    @allure.story("Проверка математической логики")
    @allure.title("Демо: Падающий тест №1 (Неверное равенство)")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Этот тест намеренно падает, для перезапуска тестов. Ожидается assert 1 == 2.")
    def test_fail_1_math_equality(self):
        with allure.step("Выполнение заведомо ложного сравнения (1 == 2)"):
            assert 1 == 2, "Ожидаемое падение: 1 не равно 2"

    @allure.story("Проверка логических операторов")
    @allure.title("Демо: Падающий тест №2 (Отрицательное сравнение)")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description("Этот тест намеренно падает, для перезапуска тестов. Ожидается assert 1 < 0.")
    def test_fail_2_math_comparison(self):
        with allure.step("Проверка условия: 1 меньше 0"):
            assert 1 < 0, "Ожидаемое падение: 1 не меньше 0"
