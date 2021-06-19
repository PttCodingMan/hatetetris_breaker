import time

from SingleLog.log import Logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Breaker:
    def __init__(self):
        self.logger = Logger('breaker', Logger.INFO)
        self.driver = webdriver.Chrome('chromedriver')
        self.driver.set_page_load_timeout(100)
        self.driver.delete_all_cookies()
        self.wait = WebDriverWait(self.driver, 10)

    def press_button(self, func_name: str):
        # self.driver.find_element(By.CSS_SELECTOR, ".e2e__left").click()
        # self.driver.find_element(By.CSS_SELECTOR, ".e2e__down").click()
        # self.driver.find_element(By.CSS_SELECTOR, ".e2e__right").click()
        # self.driver.find_element(By.CSS_SELECTOR, ".e2e__up").click()

        func_name_list = [
            'start', 'left', 'down', 'right', 'up', 'back'
        ]
        func_name = func_name.lower()
        if func_name not in func_name_list:
            raise ValueError
        if func_name == 'back':
            self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .game__button:nth-child(1)").click()
        if func_name == 'start':
            self.driver.find_element(By.CSS_SELECTOR, f".e2e__{func_name}-button").click()
        else:
            self.driver.find_element(By.CSS_SELECTOR, f".e2e__{func_name}").click()

    def show(self):
        elements = self.driver.find_elements_by_xpath("//td[contains(@class, 'well__cell')]")

        for i in range(len(elements)):
            current_state = elements[i].get_attribute('class')
            if current_state == 'well__cell':
                print('  ', end='')
            elif current_state == 'well__cell well__cell--live':
                print('▇▇', end='')
            elif current_state == 'well__cell well__cell--bar':
                # print('ㄧ', end='')
                pass
            if i % 10 == 9:
                print('')
        print('-----')

    def count(self):

        self.driver.get("https://qntm.org/files/hatetris/hatetris.html")
        self.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//script[@src='https://statcounter.com/counter/counter_xhtml.js']")
            ))
        self.logger.info('Load', 'success')
        self.press_button('start')
        self.show()

        self.press_button('left')
        self.show()
        try:
            pass
        finally:
            self.driver.close()


if __name__ == '__main__':
    logger = Logger('main', Logger.INFO)

    breaker = Breaker()
    breaker.count()
