import logging

import pytest
from selenium.webdriver import Chrome, Firefox


@pytest.fixture()
def selenium_driver(request) :
    driver = Chrome() if request.param == 'chrome' else Firefox()
    yield driver
    driver.quit()