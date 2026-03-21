from config.pydantic_config import settings


class Links:
    BASE_PAGE = settings.base_url
    REG_PAGE = settings.get_full_url("/angularjs-protractor/registeration/#/login")
    BANK_FORM_PAGE = settings.get_full_url(
        "/angularjs-protractor/banking/registrationform.html"
    )
    BANK_MANAGER_PAGE = settings.get_full_url("/angularjs-protractor/banking/#/manager")
    BANK_CUSTOMER_PAGE = settings.get_full_url(
        "https://www.way2automation.com/angularjs-protractor/banking/#/customer"
    )
