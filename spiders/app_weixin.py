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

    def slide_screen(self, type, x, y):
        # 参数说明：起始x，起始y, 终点x, 终点y，时间, 以屏幕左上角为(0,0)点
        if type == 'up':
            self.driver.swipe(1 / 2 * x, 1 / 2 * y, 1 / 2 * x, 1 / 7 * y, 200)
        elif type == 'down':
            self.driver.swipe(1 / 2 * x, 1 / 7 * y, 1 / 2 * x, 1 / 2 * y, 200)
        elif type == 'left':
            self.driver.swipe(6 / 7 * x, 1 / 2 * y, 1 / 7 * x, 1 / 2 * y, 200)
        else:
            self.driver.swipe(1 / 7 * x, 1 / 2 * y, 5 / 7 * x, 1 / 2 * y, 200)

    def run(self):
        time.sleep(2)
        x = self.driver.get_window_size()['width']
        # 获取屏幕宽
        y = self.driver.get_window_size()['height']
        self.slide_screen('left', x, y)
        time.sleep(2)
        self.slide_screen('left', x, y)
        time.sleep(2)
        self.driver.find_element_by_android_uiautomator('new UiSelector().textContains("通讯录")').click()
        time.sleep(1)
        self.driver.find_element_by_android_uiautomator('new UiSelector().textContains("公众号")').click()
        time.sleep(2)

        # for i in range(60):
        #     try:
        #         time.sleep(10)
        #         self.wait_by_key('com.tencent.mm:id/p9').click()
        #     except Exception as e:
        #         print('未获取返回键, wrong:{}'.format(e))
        #     time.sleep(10)
        #     self.driver.find_element_by_android_uiautomator('new UiSelector().textContains("查看全部MCN机构")').click()
        #     print('-----', i)
            # self.slide_screen('up', x, y)
        # self.wait.until(EC.presence_of_all_elements_located((By.ID, 'android:id/title')))[-2].click()
        # self.wait_by_key('com.tencent.mm:id/l0').click()
        # btn_search = self.wait_by_key('com.tencent.mm:id/li')
        # btn_search.send_keys('抖大大')
        # time.sleep(1)
        # self.driver.keyevent('66')
        # time.sleep(5)
        # self.driver.find_element_by_android_uiautomator('new UiSelector().textContains("抖音数据小助手，专注于抖音数据服务，更多详细数据，移步到抖大大官网www.bigdouyin.com查看")').click()


if __name__ == '__main__':
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = '5.1'
    desired_caps['deviceName'] = 'G6BELRFI99999999'
    desired_caps['appPackage'] = 'com.tencent.mm'
    desired_caps['appActivity'] = '.ui.LauncherUI'
    desired_caps['noReset'] = True # 使用缓存
    AppControl(desired_caps=desired_caps).run()

