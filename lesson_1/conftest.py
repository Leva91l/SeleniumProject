import pytest
from selenium import webdriver


HOMEPAGE_URL = "https://store.steampowered.com/"

@pytest.fixture
def driver(request):
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def get_url(driver):
    driver.get(HOMEPAGE_URL)


