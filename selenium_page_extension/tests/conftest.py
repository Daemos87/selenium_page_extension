from _pytest.python import Metafunc


def pytest_generate_tests(metafunc: Metafunc):
    browsers = []
    if metafunc.definition.get_closest_marker("chrome"):
        browsers.append("chrome")
    if metafunc.definition.get_closest_marker("firefox"):
        browsers.append("firefox")
    metafunc.parametrize('selenium_driver',browsers,indirect=True)