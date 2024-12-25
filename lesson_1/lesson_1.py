import time

import faker
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

fake = faker.Faker()


class TestSteamLoginForm:
    URL_PAGE = "https://store.steampowered.com/"
    TIMEOUT = 10
    HOME_PAGE_LOGIN_BUTTON = (By.XPATH, "//*[@id='global_action_menu']//a[@class='global_action_link']")
    # Очень длинный локатор, так можно? Просто проблема в том что все что выше - это куча divов с единственным атрибутом class автогенерируемым.
    # Никак не привязаться иначе.↓↓↓
    LOGIN_FIELD = (By.XPATH,
                   "//input[@type='text' and not(contains(@id, 'authcode')) and not(contains(@id, 'friendlyname')) and not(contains(@id, 'twofactorcode_entry'))]")
    PASSWORD_FIELD = (By.XPATH, "//input[@type='password']")
    #С кнопкой войти меняющейся на кнопку загрузки у меня не получилось никак кроме как использовать классы
    #Ничего кроме классов не меняется у них. По сути это одна кнопка меняющая стиль↓↓↓
    SIGN_IN_BUTTON = (By.XPATH, "//button[@class='DjSvCZoKKfoNSmarsEcTS']")
    LOADING_BUTTON = (
        By.XPATH, "//button[@class='DjSvCZoKKfoNSmarsEcTS _2NVQcOnbtdGIu9O-mB9-YE']")
    # здесь та же проблема, можно зацепиться за form, но дальше так же куча divов с единственным атрибутом class автогенерируемым.
    # что лучше - индекс или класс??↓↓↓
    WRONG_LOGIN_TEXT = (By.XPATH, "(//form/div)[5]")

    @staticmethod
    def page_loading_assertation(driver):
        timeout = 10
        end_time = time.time() + timeout
        while time.time() < end_time:
            # кстати, ничего не работало, пока return не добавил ↓↓↓ Зато разобрался =)
            result = driver.execute_script('return document.readyState')
            if result != "complete":
                time.sleep(1)
                end_time = end_time - 1
            else:
                break
        else:
            raise TimeoutError

    def test_login_steam(self, driver):
        wait = WebDriverWait(driver, 10)
        driver.get(self.URL_PAGE)
        self.page_loading_assertation(driver)
        wait.until(EC.presence_of_element_located(self.HOME_PAGE_LOGIN_BUTTON)).click()
        wait.until(EC.visibility_of_element_located(self.LOGIN_FIELD)).send_keys(fake.name())
        wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD)).send_keys(fake.password())
        wait.until(EC.element_to_be_clickable(self.SIGN_IN_BUTTON)).click()
        assert wait.until(EC.invisibility_of_element(self.SIGN_IN_BUTTON))
        assert wait.until(EC.visibility_of_element_located(self.LOADING_BUTTON)).is_displayed()
        assert wait.until(EC.visibility_of_element_located(self.SIGN_IN_BUTTON))
        assert wait.until(EC.text_to_be_present_in_element(
            self.WRONG_LOGIN_TEXT, 'Пожалуйста, проверьте свой пароль и имя аккаунта и попробуйте снова.'))
