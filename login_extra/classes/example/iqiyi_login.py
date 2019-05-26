import cv2

from classes import analog_login
from tool.warpper import warning, read_ad_cookies
from settings.conf import *
from PIL import Image
from urllib import parse
from io import BytesIO
from settings import plats_conf
from datetime import datetime, timedelta
import time
import numpy as np


class IqiyiLogin(analog_login.AnalogLogin):
    verify_cookie_url = 'https://tuiguang.iqiyi.com/advertiserAccount/index?targetUri='

    def __init__(self, acc, pwd, driver, *args, **kwargs):
        super(IqiyiLogin, self).__init__(driver=driver, plat='iqiyi', *args, **kwargs)
        self.acc_xpath = '//*[@id="user"]'
        self.pwd_xpath = '//*[@id="psw"]'
        self.login_url = 'https://tuiguang.iqiyi.com'
        self.acc = acc
        self.pwd = pwd
        self.mark_times = 0
        self.zoom = 1

    def before_login(self):
        self.wait_el_presence_by_xpath('//*[@id="btn-entry"]').click()

    def verify_cookie(self):
        self.browser.get(self.verify_cookie_url)
        time.sleep(2)
        return 'login' not in self.browser.current_url.lower()

    def after_login(self):
        time.sleep(2)
        self.browser.get(self.verify_cookie_url)
        time.sleep(2)
        return 'login' not in self.browser.current_url.lower()

    def enter(self):
        flag_success = False
        while not flag_success and self.mark_times < 8:
            # 下载完整的验证图
            target = DIR_ + 'iqiyi_target.png'
            template = DIR_ + 'iqiyi_template.png'
            image_target = self.get_image("jigsaw-bg", target)
            # 下载有缺口的验证图
            image_block = self.get_block_img('jigsaw-block', template)
            # 确定缺口位置
            distance = self.match(target, template)
            # pdb.set_trace()
            tracks = self.get_tracks((distance + 7 )*self.zoom)
            result = self.simulate_drag(tracks)
            print(result)

            self.mark_times += 1
            if result:
                flag_success = True
            else:
                dom_div_slider = self.browser.find_element_by_id('test')
                ActionChains(self.browser).move_to_element(dom_div_slider).perform()
                time.sleep(1)
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'refresh'))).click()
                time.sleep(1)

        if flag_success:
            self.wait.until(EC.presence_of_element_located((By.ID, 'btn-login'))).click()

    def get_block_img(self, class_name, template):
        div_style = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name))).get_attribute('style')
        image_url = re.findall('background-image: url\("(.*?)"\);', div_style)[0]
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
        response = requests.get(image_url, headers=headers, verify=False)
        image = Image.open(BytesIO(response.content))
        image.save(template)

    def get_image(self, class_name, target):
        """
        下载并还原极验的验证图
        Args:
            class_name: 验证图所在的html标签的class name
        Returns:
            返回验证图
        Errors:
            IndexError: list index out of range. ajax超时未加载完成，导致image_slices为空
        """

        image_slices = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="{}"]/div[position()<last()]'.format(class_name))))
        # print(len(image_slices))

        # pdb.set_trace()
        if len(image_slices) == 0:
            print('No such a class')
        div_style = image_slices[0].get_attribute('style')
        # pdb.set_trace()
        image_url = re.findall('background-image: url\("(.*?)"\); background-position: (.*?)px *(.*?)px;', div_style)[0][0]
        image_filename = parse.urlsplit(image_url).path.split('/')[-1]
        location_list = list()
        for image_slice in image_slices:
            location = dict()
            location['x'] = int(re.findall('background-image: url\("(.*?)"\); background-position: (.*?)px *(.*?)px;', image_slice.get_attribute('style'))[0][1])
            location['y'] = int(re.findall('background-image: url\("(.*?)"\); background-position: (.*?)px *(.*?)px;', image_slice.get_attribute('style'))[0][2])
            location_list.append(location)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
        response = requests.get(image_url, headers=headers, verify=False)

        image = Image.open(BytesIO(response.content))
        self.recover_image(image, location_list, target)

    def recover_image(self, image, location_list, target):
        """
        还原验证图像
        Args:
            image: 打乱的验证图像（PIL.Image数据类型）
            location_list: 验证图像每个碎片的位置
        Returns:
           还原过后的图像
        """
        new_im = Image.new('RGB', (240, 150))
        im_list_upper = []
        im_list_down = []
        for location in location_list:
            if location['y'] == 0:
                im_list_upper.append(image.crop((abs(location['x']), 0, abs(location['x']) + 12, 75)))
            if location['y'] == 75:
                im_list_down.append(image.crop((abs(location['x']), 75, abs(location['x']) + 12, 150)))

        x_offset = 0
        for im in im_list_upper:
            new_im.paste(im, (x_offset, 0))
            x_offset += im.size[0]

        x_offset = 0
        for im in im_list_down:
            new_im.paste(im, (x_offset, 75))
            x_offset += im.size[0]
        new_im.save(target)

    def match(self, target, template):
        img_rgb = cv2.imread(target)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template, 0)
        run = 1
        w, h = template.shape[::-1]
        # print(w, h)

        method = cv2.TM_CCOEFF_NORMED
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(img_rgb, top_left, bottom_right, 255, 2)
        cv2.imwrite('match.png', img_rgb)
        # print(top_left)
        # 使用二分法查找阈值的精确值
        L = 0
        R = 1
        while run < 20:
            run += 1
            threshold = (R + L) / 2
            # print(threshold)
            if threshold < 0:
                print('Error')
                return None
            loc = np.where(res >= threshold)
            # print(len(loc[1]))
            if len(loc[1]) > 1:
                L += (R - L) / 2
            elif len(loc[1]) == 1:
                print('目标区域起点x坐标为：%d' % loc[1][0])
                break
            elif len(loc[1]) < 1:
                R -= (R - L) / 2

        return loc[1][0]

    def get_tracks(self, distance):
        distance += 20
        v = 0
        t = 0.2
        forward_tracks = []
        current = 0
        mid = distance * 3 / 5
        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3
            s = v * t + 0.5 * a * (t ** 2)
            v = v + a * t
            current += s
            forward_tracks.append(round(s))

        back_tracks = [-3,-3,-2,-2,-2,-2,-2,-1,-1,-1]
        return {'forward_tracks': forward_tracks, 'back_tracks': back_tracks}

    def simulate_drag(self, tracks):

        dom_div_slider = self.browser.find_element_by_id('test')

        ActionChains(self.browser).click_and_hold(dom_div_slider).perform()

        for track in tracks['forward_tracks']:
            ActionChains(self.browser).move_by_offset(xoffset=track, yoffset=0).perform()

        time.sleep(0.5)
        for back_tracks in tracks['back_tracks']:
            ActionChains(self.browser).move_by_offset(xoffset=back_tracks, yoffset=0).perform()

        ActionChains(self.browser).move_by_offset(xoffset=-3, yoffset=0).perform()
        ActionChains(self.browser).move_by_offset(xoffset=3, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()
        time.sleep(1)
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'verify-success')]")))
        except:
            return False
        else:
            return True


