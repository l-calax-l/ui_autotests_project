from selenium.webdriver.common.by import By

from base.base_page import BasePage
from config.links import Links


class DroppablePage(BasePage):
    """Page Object для страницы с Drag n Drop (IFrame)."""

    PAGE_PATH = Links.DROP_PAGE

    IFRAME = (By.CSS_SELECTOR, "#example-1-tab-1 iframe")
    DRAGGABLE = (By.ID, "draggable")
    DROPPABLE = (By.ID, "droppable")

    def drag_element_to_target(self):
        self.drag_and_drop(self.DRAGGABLE, self.DROPPABLE)
