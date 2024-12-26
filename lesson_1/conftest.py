import pytest
from selenium import webdriver

@pytest.fixture(autouse=True)
def driver(request):
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def get_url(driver):
    driver.get("https://store.steampowered.com/")
