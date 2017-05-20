import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def login_to_site(driver, username, password):
    element = driver.find_element_by_id('login-trigger')
    element.click()

    element = driver.find_element_by_id("Username")
    WebDriverWait(driver, 10).until(expected_conditions.visibility_of(element))
    element.send_keys(username)

    element = driver.find_element_by_id('Password')
    element.send_keys(password)

    element = driver.find_element_by_id('Login')
    element.click()


def logout_of_site(driver):
    element = driver.find_element_by_id("account-icon")
    WebDriverWait(driver, 10).until(expected_conditions.visibility_of(element))
    element.click()

    element = driver.find_element_by_id("btnLogout")
    WebDriverWait(driver, 10).until(expected_conditions.visibility_of(element))
    element.click()

    element = driver.find_element_by_id('login-trigger')
    WebDriverWait(driver, 10).until(expected_conditions.visibility_of(element))


def wait_until_clickable(driver, xpath_selector):
    def stopped_moving(driver):
        try:
            element = driver.find_element_by_xpath(xpath_selector)
            WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, xpath_selector)))
            initial = (element.location, element.size)
            time.sleep(0.5)
            element = driver.find_element_by_xpath(xpath_selector)
            final = (element.location, element.size)
            return initial == final
        except Exception as e:
            print(e)
            return False

    WebDriverWait(driver, 10).until(stopped_moving)
    return driver.find_element_by_xpath(xpath_selector)


def wait_until_browser_close(driver):
    while True:
        try:
            _ = driver.title
            time.sleep(1)
        except Exception as e:
            print(e)
            break
