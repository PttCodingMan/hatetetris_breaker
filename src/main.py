from SingleLog.log import Logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# https://qntm.org/files/hatetris/hatetris.html
class Breaker:
    def __init__(self):
        self.logger = Logger('breaker', Logger.INFO)
        self.driver = webdriver.Chrome('chromedriver')
        self.driver.set_page_load_timeout(100)
        self.driver.delete_all_cookies()
        self.wait = WebDriverWait(self.driver, 10)

        self.last_down_state = True

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
        elif func_name == 'start':
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
            elif current_state == 'well__cell well__cell--landed':
                print('▇▇', end='')
            elif current_state == 'well__cell well__cell--bar':
                # print('ㄧ', end='')
                pass
            else:
                print(current_state)
            if i % 10 == 9:
                print('')
        print('-----')

    def is_live(self):
        elements = self.driver.find_elements_by_xpath("//td[contains(@class, 'well__cell')]")
        for e in elements:
            current_state = e.get_attribute('class')
            if 'live' in current_state:
                return True
        return False

    def has_new_cube(self):
        elements = self.driver.find_elements_by_xpath("//td[contains(@class, 'well__cell')]")[14:20]
        for e in elements:
            current_state = e.get_attribute('class')
            if 'live' in current_state:
                return True
        return False

    def is_down(self):
        current_new_state = self.has_new_cube()
        if not self.last_down_state and current_new_state:
            self.last_down_state = True
            return self.last_down_state
        self.last_down_state = False
        return self.last_down_state

    def down_util_end(self):
        step_count = 0
        while not self.is_down():
            self.press_button('down')
            step_count += 1
        return step_count

    def reset(self, step_count):
        for _ in range(step_count):
            self.press_button('back')

    def get_dis_from_left(self):
        elements = self.driver.find_elements_by_xpath("//td[contains(@class, 'well__cell')]")
        result = 10
        for i in range(len(elements)):
            current_state = elements[i].get_attribute('class')
            if current_state != 'well__cell well__cell--live':
                continue
            current_i = i % 10
            result = min(result, current_i)
        return result

    def get_dis_from_right(self):
        elements = self.driver.find_elements_by_xpath("//td[contains(@class, 'well__cell')]")
        result = 0
        for i in range(len(elements)):
            current_state = elements[i].get_attribute('class')
            if current_state != 'well__cell well__cell--live':
                continue
            current_i = i % 10
            result = max(result, current_i)
        return 9 - result

    def move_to_x(self, x):
        last_x = current_x = self.get_dis_from_left()

        step_count = 0
        while current_x != x:
            if x < current_x:
                self.press_button('left')
            elif current_x < x:
                self.press_button('right')
            step_count += 1
            current_x = self.get_dis_from_left()

            if last_x == current_x:
                break
            last_x = current_x

        return step_count

    def count(self):

        self.driver.get("https://qntm.org/files/hatetris/hatetris.html")
        self.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//script[@src='https://statcounter.com/counter/counter_xhtml.js']")
            ))
        self.logger.info('Load', 'success')
        self.press_button('start')
        self.show()

        for i in range(10):
            step_count = self.move_to_x(i)
            self.show()
            if self.get_dis_from_right() == 0:
                self.reset(step_count)
                break
            self.reset(step_count)
        try:
            pass
        finally:
            self.driver.close()


if __name__ == '__main__':
    logger = Logger('main', Logger.INFO)

    breaker = Breaker()
    breaker.count()
