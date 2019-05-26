from PIL import Image, ImageEnhance
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import cv2
import numpy as np
from io import BytesIO
import time, requests


class CrackSlider(object):
    """
    通过浏览器截图，识别验证码中缺口位置，获取需要滑动距离，并模仿人类行为破解滑动验证码
    """
    def __init__(self, browser, plat, speed, target_xpath, tem_xpath, bias, slider_xpath, reload_xpath, retry_times=5, acc=''):
        super(CrackSlider, self).__init__()
        # 实际地址
        self.driver = browser
        self.wait = WebDriverWait(self.driver, 20)
        self.zoom = 1
        self.mark = 0
        self.plat = plat
        self.speed = speed  # 0.2
        self.target_xpath = target_xpath
        self.tem_xpath = tem_xpath
        self.bias = bias  # -25
        self.slider_xpath = slider_xpath
        self.reload_xpath = reload_xpath
        self.retry_times = retry_times
        self.target_file_name = self.plat + '_{}_'.format(acc) + 'target.jpg'
        self.temp_file_name = self.plat + '_{}_'.format(acc) + 'template.png'
        self.match_file_name = self.plat + '_{}_'.format(acc) + 'match.png'

    def get_pic(self):
        time.sleep(2)
        target = self.wait.until(EC.presence_of_element_located((By.XPATH, self.target_xpath)))
        template = self.wait.until(EC.presence_of_element_located((By.XPATH, self.tem_xpath)))

        target_link = 'https://captcha.guard.qcloud.com' + target.get_attribute('src')
        template_link = 'https://captcha.guard.qcloud.com' + template.get_attribute('src')

        target_img = Image.open(BytesIO(requests.get(target_link).content))
        template_img = Image.open(BytesIO(requests.get(template_link).content))
        target_img.save(self.target_file_name)
        template_img.save(self.temp_file_name)
        size_orign = target.size
        local_img = Image.open(self.target_file_name)
        size_loc = local_img.size
        self.zoom = 320 / int(size_loc[0])

    def get_tracks(self, distance):
        print(distance)
        if self.plat == 'ks':
            distance -= self.bias
        v = 0
        t = self.speed
        forward_tracks = []
        current = 0
        mid = distance * 3/5
        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3
            s = v * t + 0.5 * a * (t**2)
            v = v + a * t
            current += s
            forward_tracks.append(round(s))

        back_tracks = [-3,-3,-2,-2,-2,-2,-2,-1,-1,-1]
        return {'forward_tracks':forward_tracks,'back_tracks':back_tracks}

    def match(self, target, template):
        img_rgb = cv2.imread(target)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template,0)
        run = 1
        w, h = template.shape[::-1]
        print(w, h)

        method = cv2.TM_CCOEFF_NORMED
        res = cv2.matchTemplate(img_gray,template,cv2.TM_SQDIFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(img_rgb, top_left, bottom_right, 255, 2)
        cv2.imwrite(self.match_file_name,img_rgb)

        # 使用二分法查找阈值的精确值
        L = 0
        R = 1
        while run < 20:
            run += 1
            threshold = (R + L) / 2
            print(threshold)
            if threshold < 0:
                print('Error')
                return None
            loc = np.where( res >= threshold)
            print(len(loc[1]))
            if len(loc[1]) > 1:
                L += (R - L) / 2
            elif len(loc[1]) == 1:
                print('目标区域起点x坐标为：%d' % loc[1][0])
                break
            elif len(loc[1]) < 1:
                R -= (R - L) / 2

        return loc[1][0]

    def crack_slider(self):
        target = self.target_file_name
        template = self.temp_file_name
        self.get_pic()
        distance = self.match(target, template)
        tracks = self.get_tracks((distance + 7 )*self.zoom) # 对位移的缩放计算

        slider = self.wait.until(EC.presence_of_element_located((By.XPATH, self.slider_xpath)))
        ActionChains(self.driver).click_and_hold(slider).perform()

        for track in tracks['forward_tracks']:
            ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()

        time.sleep(0.5)
        for back_tracks in tracks['back_tracks']:
            ActionChains(self.driver).move_by_offset(xoffset=back_tracks, yoffset=0).perform()

        ActionChains(self.driver).move_by_offset(xoffset=-3, yoffset=0).perform()
        ActionChains(self.driver).move_by_offset(xoffset=3, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.driver).release().perform()
        try:
            time.sleep(5)
            failure = self.driver.find_element_by_xpath(self.slider_xpath)
        except:
            print('验证成功')
            return None

        if failure and self.mark < 5:
            self.mark += 1
            self.driver.find_element_by_xpath(self.reload_xpath).click()
            self.crack_slider()


if __name__ == '__main__':
    pass