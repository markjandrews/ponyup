import weakref

import sys

import time

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from ponyup.common import login_to_site, logout_of_site, wait_until_clickable


class PowerBallDraw(object):
    def __init__(self, driver, user_name, password):
        self.driver = driver

        driver.get('https://thelott.com/nswlotteries')
        assert driver.title == 'NSW Lotteries | Official Lottery Site for NSW | the Lott Australia\'s Official Lotteries'

        login_to_site(driver, user_name, password)

        driver.get('https://thelott.com/nswlotteries/buy-lotto/purchase-ticket?product=Powerball')
        driver.find_element_by_xpath(
            "//div[@id='StandardGamesDiv']").click()

    def close(self):
        print('Logging out and closing browser')
        sys.stdout.flush()
        logout_of_site(self.driver)
        self.driver.close()
        print('Browser Closed')
        sys.stdout.flush()

    def set_num_games(self, num_games):
        assert 4 < num_games <= 50

        self.driver.find_element_by_xpath(
            "//div[@id='StandardGamesDiv']/table/tbody/tr/td/select[@id='StandardGameCountSel']/option[@value='%s']" %
            num_games).click()

    def set_games(self, picked_list):
        self.set_num_games(len(picked_list))

        for i in range(len(picked_list)):
            self.driver.find_element_by_xpath(
                "//table[@id='GameSelectionsTbl']/tbody/tr/td/div/span[.='%s']" % (i + 1)).click()

            selection_table = wait_until_clickable(self.driver, "//table[@id='GridSelectionsTbl']")
            WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of(selection_table))

            for j in range(len(picked_list[i][0])):
                element = selection_table.find_element_by_xpath(".//td[@selection='%s']" % picked_list[i][0][j])
                element.click()

            self.driver.find_element_by_xpath(
                "//table[@id='GameSelectionsTbl']/tbody/tr[@class='gameRow selected']/td/div/select[@class="
                "'gamePowerballSel']/option[@value='%s']" % picked_list[i][1][0]).click()
