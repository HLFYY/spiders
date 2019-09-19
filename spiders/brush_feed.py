import sys
import time
import re
import redis
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AppControl():
    def __init__(self, desired_caps):
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        self.wait = WebDriverWait(self.driver, 10)

    def wait_by_key(self, key='', by_type=By.ID, ):
        return self.wait.until(EC.presence_of_element_located((by_type, key)))

    def get_element_by_word(self, word):
        return self.driver.find_element_by_android_uiautomator('new UiSelector().textContains("%s")'%word)

    def slide_screen(self, type, x, y):
        # 参数说明：起始x，起始y, 终点x, 终点y，时间, 以屏幕左上角为(0,0)点
        if type == 'up':
            self.driver.swipe(1 / 2 * x, 1 / 2 * y, 1 / 2 * x, 1 / 7 * y, 200)
        elif type == 'down':
            self.driver.swipe(1 / 2 * x, 2 / 5 * y, 1 / 2 * x, 4 / 5 * y, 200)
        elif type == 'left':
            self.driver.swipe(6 / 7 * x, 1 / 2 * y, 1 / 7 * x, 1 / 2 * y, 200)
        else:
            self.driver.swipe(1 / 7 * x, 1 / 2 * y, 5 / 7 * x, 1 / 2 * y, 200)

    def run_weili(self):
        time.sleep(8)
        self.get_element_by_word('推荐').click()

        while True:
            time.sleep(15)
            x = self.driver.get_window_size()['width']
            # 获取屏幕宽
            y = self.driver.get_window_size()['height']
            print('--微鲤刷新, time:{}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
            self.slide_screen('down', x, y)


if __name__ == '__main__':
    platform = sys.argv[1]
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = '5.1'
    desired_caps['deviceName'] = 'G6BELRFI99999999'
    desired_caps['noReset'] = True # r456t使用缓存
    if platform == 'weili':
        desired_caps['appPackage'] = 'cn.weli.story'
        desired_caps['appActivity'] = 'cn.etouch.ecalendar.MainActivity'
        print(desired_caps)

        AppControl(desired_caps=desired_caps).run_weili()
    elif platform == 'east':
        desired_caps['appPackage'] = 'com.songheng.eastnews'
        desired_caps['appActivity'] = 'com.songheng.eastfirst.common.view.activity.MainActivity'
        print(desired_caps)
        AppControl(desired_caps=desired_caps).run_weili()


