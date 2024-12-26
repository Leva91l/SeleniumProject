import time

import faker
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

fake = faker.Faker()


class TestSteamLoginForm:
    TIMEOUT = 10
    HOME_PAGE_LOGIN_BUTTON = (By.XPATH,
                              "//*[@id='global_action_menu']/a[not(contains(@class, 'header_installsteam_btn_green')) or not(contains(@class, 'header_installsteam_btn'))]")
    LOGIN_FIELD = (By.XPATH,
                   "//input[@type='text' and not(contains(@id, 'authcode')) and not(contains(@id, 'friendlyname')) and not(contains(@id, 'twofactorcode_entry'))]")
    PASSWORD_FIELD = (By.XPATH, "//input[@type='password']")

    # слушай, ну еще вот такой вариант, ну если уже и это нет, тогда надо чтоб ты показал и объянил на этом примере наверное↓↓↓
    SIGN_IN_BUTTON = (By.XPATH, "//form//div//button[not(contains(@class, '_2NVQcOnbtdGIu9O-mB9-YE'))]")
    LOADING_BUTTON = (
        By.XPATH, "//button[contains(@class, '_2NVQcOnbtdGIu9O-mB9-YE')]")

    WRONG_LOGIN_TEXT = (By.XPATH, "(//form/div)[5]")

    @staticmethod
    def page_loading_assertation(driver):
        timeout = 10
        end_time = time.time() + timeout
        while time.time() < end_time:
            result = driver.execute_script('return document.readyState')
            if result != "complete":
                time.sleep(1)
            else:
                break
        else:
            raise TimeoutError

    def test_login_steam(self, driver, get_url):
        wait = WebDriverWait(driver, 10)
        self.page_loading_assertation(driver)
        wait.until(EC.presence_of_element_located(self.HOME_PAGE_LOGIN_BUTTON)).click()
        wait.until(EC.visibility_of_element_located(self.LOGIN_FIELD)).send_keys(fake.name())
        wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD)).send_keys(fake.password())
        wait.until(EC.element_to_be_clickable(self.SIGN_IN_BUTTON)).click()
        wait.until(EC.invisibility_of_element(self.SIGN_IN_BUTTON))
        assert wait.until(EC.visibility_of_element_located(self.LOADING_BUTTON))
        wait.until(EC.visibility_of_element_located(self.SIGN_IN_BUTTON))
        wait.until(EC.visibility_of_element_located(self.WRONG_LOGIN_TEXT))
        wrong_text = driver.find_element(*self.WRONG_LOGIN_TEXT).text
        assert wrong_text == 'Пожалуйста, проверьте свой пароль и имя аккаунта и попробуйте снова.'
