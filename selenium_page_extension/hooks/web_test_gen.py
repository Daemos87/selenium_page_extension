import logging

from _pytest.python import Metafunc
# noinspection PyUnresolvedReferences
from ..fixtures.selenium_fixture import selenium_driver

logger = logging.getLogger(__name__)


def pytest_configure(config):
    # register an additional marker
    config.addinivalue_line(
        "markers", "chrome")

    config.addinivalue_line(
        "markers", "firefox"
    )


def pytest_generate_tests(metafunc: Metafunc):
    if 'selenium_driver' not in metafunc.fixturenames:
        return
    browsers = []
    if mark := metafunc.definition.get_closest_marker("chrome"):
        browsers.append(("chrome", mark.args))
    if metafunc.definition.get_closest_marker("firefox"):
        browsers.append(("firefox", mark.args))
    metafunc.parametrize('selenium_driver', browsers, indirect=True)
