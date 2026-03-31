from base.base_page import BasePage
from config.links import Links


class DroppablePage(BasePage):
    """Page Object для страницы с Drag n Drop (IFrame)."""

    PAGE_PATH = Links.DROP_PAGE

    IFRAME = ("css selector", "#example-1-tab-1 iframe")
    DRAGGABLE = ("id", "draggable")
    DROPPABLE = ("id", "droppable")
