import allure
import pytest

from base.base_test import BaseTest


@pytest.mark.website
@pytest.mark.droppable
@allure.epic("Взаимодействие с элементами")
class TestDropPage(BaseTest):
    """Тестовый класс для проверки Drag n Drop."""

    @pytest.mark.smoke
    @allure.feature("Drag n Drop")
    @allure.story("Перетаскивание в IFrame")
    @allure.title("Успешное перемещение элемента в область Droppable")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_1_drag_n_drop(self):
        self.drop_page.open()

        with allure.step("Переключиться на iframe"):
            self.drop_page.switch_to_frame(self.drop_page.IFRAME)

        with allure.step("Запомнить текст принимающего элемента до Drop"):
            text_before = self.drop_page.get_text(self.drop_page.DROPPABLE)

        with allure.step("Перетащить элемент 'Draggable' в область 'Droppable'"):
            self.drop_page.drag_and_drop(
                self.drop_page.DRAGGABLE, self.drop_page.DROPPABLE
            )

        with allure.step("Убедиться, что текст принимающего элемента изменился"):
            text_after = self.drop_page.get_text(self.drop_page.DROPPABLE)

            assert (
                text_before != text_after
            ), f"Текст не изменился! До: '{text_before}', После: '{text_after}'"

            assert (
                text_after == "Dropped!"
            ), f"Ожидался текст 'Dropped!', получили '{text_after}'"
