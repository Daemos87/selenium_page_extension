import logging
from abc import ABC
from typing import Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
import configparser

conf = configparser.ConfigParser()

conf.read("selenium_extension.ini")

wait_presence = conf.getint("selenium_ext","wait_for_presence",fallback=20)

class WebPage(ABC) :

    def __init__(self, driver: WebDriver) :
        self._driver: WebDriver = driver
        self._wait: WebDriverWait = WebDriverWait(driver, wait_presence)
        logging.getLogger("").critical(wait_presence)

    def __getattribute__(self, item: str) :
        class_ref = super().__getattribute__('__class__')
        typ = class_ref.__annotations__.get(item, None)
        locator = class_ref.__dict__.get(item, None)

        # not a private member
        # and the member is initialized ( with a WebElement locator hopefully)
        # member type hint is WebElement or a tuple[WebElement]
        if not item.startswith('_') \
                and locator \
                and typ in [WebElement, Tuple[WebElement]]:

            method = ec.presence_of_element_located if typ == WebElement else ec.presence_of_all_elements_located
            return super().__getattribute__('_wait').until(method(locator))

        return super().__getattribute__(item)
