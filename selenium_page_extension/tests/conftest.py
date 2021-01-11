from datetime import datetime

import pytest
from _pytest.python import Metafunc


def pytest_generate_tests(metafunc: Metafunc) :
    if not 'selenium_driver' in metafunc.fixturenames:
        return
    browsers = []
    if metafunc.definition.get_closest_marker("chrome") :
        browsers.append("chrome")
    if metafunc.definition.get_closest_marker("firefox") :
        browsers.append("firefox")
    metafunc.parametrize('selenium_driver', browsers, indirect=True)


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call) :
    timestamp = datetime.now().strftime('%H-%M-%S')

    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call' :
        if not   'selenium_driver' in item.fixturenames:
            return

        feature_request = item.funcargs['request']

        driver = feature_request.getfixturevalue('selenium_driver')

        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail) :
            b64 = driver.get_screenshot_as_base64()
            extra.append(pytest_html.extras.image(b64))
        report.extra = extra
