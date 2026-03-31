from config.pydantic_config import settings


class Links:
    """Класс для хранения URL-адресов тестируемых приложений."""

    BASE_PAGE_1: str = settings.base_url_1
    """Главная страница приложения."""

    REG_PAGE: str = settings.get_full_url(
        BASE_PAGE_1, "/angularjs-protractor/registeration/#/login"
    )
    """Страница регистрации/логина."""

    BANK_FORM_PAGE: str = settings.get_full_url(
        BASE_PAGE_1, "/angularjs-protractor/banking/registrationform.html"
    )
    """Страница формы регистрации в банковском приложении."""

    BANK_MANAGER_PAGE: str = settings.get_full_url(
        BASE_PAGE_1, "/angularjs-protractor/banking/#/manager"
    )
    """Страница менеджера банка."""

    BANK_CUSTOMER_PAGE: str = settings.get_full_url(
        BASE_PAGE_1, "/angularjs-protractor/banking/#/customer"
    )
    """Страница клиента банка."""

    BASE_PAGE_2 = settings.base_url_2

    DROP_PAGE: str = settings.get_full_url(
        BASE_PAGE_1, "/way2auto_jquery/droppable.php"
    )

    TABS_PAGE: str = settings.get_full_url(
        BASE_PAGE_1, "/way2auto_jquery/frames-and-windows.php"
    )
