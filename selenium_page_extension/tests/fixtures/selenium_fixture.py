import pytest
from selenium.webdriver import Chrome


@pytest.fixture()
def selenium_driver():
    driver = Chrome()
    yield driver
    driver.quit()
