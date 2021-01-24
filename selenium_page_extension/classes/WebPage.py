from abc import ABC
from typing import Tuple, Type

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from typing import Any

from selenium_page_extension.classes import wait_presence
from selenium_page_extension.classes.WebElementWrapper import WebElementWrapper


class WebPage(ABC) :

    def __init__(self, driver: WebDriver) :
        self._driver: WebDriver = driver
        self._wait_presence: WebDriverWait = WebDriverWait(driver, wait_presence)


    def __getattribute__(self, item: str) -> Any:
        class_ref:Type[Type] = super().__getattribute__('__class__')
        try:
            typ = class_ref.__annotations__.get(item, None)
        except AttributeError:
            raise RuntimeError(f"Cannot find any type annotation on class {type(self).__name__}, look like an error, check the doc at [placeholder]")
        locator = class_ref.__dict__.get(item, None)
        message = f'cannot find element(s) identified by {locator} after {wait_presence} seconds timeout'

        # not a private member
        # and the member is initialized ( with a WebElement locator hopefully)
        if not item.startswith('_') and locator :
            if typ == WebElementWrapper :
                return WebElementWrapper(self._driver, super().__getattribute__('_wait_presence').until(
                    ec.presence_of_element_located(locator), message=message))
            elif typ == Tuple[WebElementWrapper] :
                return [WebElementWrapper(self._driver, el) for el in
                        super().__getattribute__('_wait_presence').until(ec.presence_of_all_elements_located(locator),
                                                                         message=message)]

        return super().__getattribute__(item)
