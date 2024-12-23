import pytest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture(autouse=True)
def driver(request):
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver


class TestSteamLoginForm:
    URL_PAGE = "https://store.steampowered.com/"
    HOME_PAGE_LOGIN_BUTTON = ("xpath", "//*[@id='global_action_menu']//a[contains(text(), 'войти')]")
    LOGIN_FIELD = ("xpath", "//input[contains(@class, '_2GBWeup5cttgbTw8FM3tfx') and contains(@type, 'text')]")
    PASSWORD_FIELD = ("xpath", "//input[contains(@class, '_2GBWeup5cttgbTw8FM3tfx') and contains(@type, 'password')]")
    SIGN_IN_BUTTON = ("xpath", "//button[@type='submit']")
    LOADING_BUTTON = (
        "xpath", "//*[contains(@class, 'DjSvCZoKKfoNSmarsEcTS') or contains(@class, '_2NVQcOnbtdGIu9O-mB9-YE')]")
    WRONG_LOGIN_TEXT = ("xpath", "//*[@class='_1W_6HXiG4JJ0By1qN_0fGZ']")

    def test_login_steam(self, driver):
        wait = WebDriverWait(driver, 10)
        driver.get(self.URL_PAGE)
        driver.find_element(*self.HOME_PAGE_LOGIN_BUTTON).click()
        wait.until(EC.visibility_of_element_located(self.LOGIN_FIELD)).send_keys('dskjbvid')
        # вопрос, можно ли ждать появления только одного элемента, зная что остальные же вроде как тоже должны подгрузиться
        # или нужно на каждый элемент писать явное ожидание?
        driver.find_element(*self.PASSWORD_FIELD).send_keys('<PASSWORD>')
        driver.find_element(*self.SIGN_IN_BUTTON).click()
        assert wait.until(EC.visibility_of_element_located(self.LOADING_BUTTON)).is_displayed()
        assert wait.until(EC.visibility_of_element_located(self.WRONG_LOGIN_TEXT)).is_displayed()


"""Вопросы:
1) Отличие явного от неявного иожидания - в том что явное ждет условия для одного элемента, а неявное ждет появление элемента на странице при чем применяется ко всем элементам
2) expected conditions - много разных (visibilityOfElementLocated, elementToBeClickable, presenceOfElementLocated и тд), 
    все для каких то условий(кликабельность, видимость, появления текста определенного, исчезновения элемента и тд), короче гибкий инструмент, сохранил шпаргалку себе
3) Отличие find_element от find_elements - Первый ищет первый подходящий элемент и возвращает его.
    Если не находит то генерирует искл. - NoSuchElementException
    Второй ищет все подходящие элементы, возвращает их список. Если не находит - возвращает пустой список без исключения
    Вот про их аналоги не совсем понял, можешь объяснить? Сам думаю что аналог это - presenceOfElementLocated потому что просто ищет элемент в DOM
4) Если явное ожидание не найдет элемент - TimeoutException
    Если неявное - NoSuchElementException
5) что будет, если локатор находит сразу несколько элементов - Либо работает с первым, если это возможно, если нет - то упадет с ошибкой"""
