import pytest
from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


@pytest.fixture()
def selenium_driver(request) :
    args = request.param[1]
    if request.param[0] == 'chrome' :
        opt = ChromeOptions()
        driver = Chrome
    else :
        opt = FirefoxOptions()
        driver = Firefox
    for o in args :
        opt.add_argument(o)
    driver = driver(options=opt)
    yield driver
    driver.quit()
