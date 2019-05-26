from classes import analog_login
from tool.warpper import warning, read_ad_cookies
from settings.conf import *
from PIL import Image
from urllib import parse
from io import BytesIO
from settings import plats_conf
from datetime import datetime, timedelta
import time


class BilibiliLogin(analog_login.AnalogLogin):
    verify_cookie_url = 'http://cm.bilibili.com/ad/#/ad/all/campaign'

    js = """var keys=document.cookie.match(/[^ =;]+(?=\=)/g);
            if (keys) {
            for (var i = keys.length; i--;)
            document.cookie=keys[i]+'=0;expires=' + new Date( 0).toUTCString()
            } """

    def __init__(self, acc, pwd, driver, *args, **kwargs):
        # c
        super(BilibiliLogin, self).__init__(driver=driver, plat='bilibili', *args, **kwargs)
        self.acc_xpath = '//*[@id="login-username"]'
        self.pwd_xpath = '//*[@id="login-passwd"]'
        self.login_url = 'https://passport.bilibili.com/login?gourl=http://cm.bilibili.com/ad/'
        self.acc = acc
        self.pwd = pwd
        self.mark_times = 0

    def run(self):
        """
            流程
        """
        if not self.read_browser_cookie():
            time.sleep(1)
            self.to_login()
            time.sleep(1)
            self.save_browser_cookie()
        time.sleep(1)

    def read_browser_cookie(self):
        """
            浏览器设置cookie
        """
        self.browser.delete_all_cookies()
        cookies = read_ad_cookies(self.acc, self.plat)
        cookie = ''
        for d in cookies:
            cookie += '{}={};'.format(d['name'], d['value'])
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            'Cookie': cookie,
        }
        start_time = int(str(int(time.mktime(datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d').timetuple()))) + '000')
        end_time = int(str(int(time.mktime(datetime.strptime((datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'), '%Y-%m-%d').timetuple())) - 1) + '999')
        url = 'http://cm.bilibili.com/platform/api/web_api/v1/launch/cpc/campaign/report?page=1' \
              '&page_size=20&from_time={}' \
              '&to_time={}&campaign_name='.format(start_time, end_time)

        res = requests.get(url, headers=headers, verify=False)
        print(res.status_code)
        return res.status_code == 200

    def after_login(self):
        time.sleep(2)
        try:
            el = self.wait_el_presence_by_xpath('//*[@id="app"]/div/div/div[2]/div/div/div/div[3]/button')
            ActionChains(self.browser).move_to_element(el).click().perform()
        except Exception as e:
            warning('bilibili miss click_login_redirct')
        time.sleep(3)

    def enter(self):
        flag_success = False
        while not flag_success and self.mark_times < 8:
            image_full_bg = self.get_image("gt_cut_fullbg_slice")
            # 下载完整的验证图
            image_bg = self.get_image("gt_cut_bg_slice")
            # 下载有缺口的验证图
            diff_x = self.get_diff_x(image_full_bg, image_bg)
            # pdb.set_trace()
            track = self.get_track(diff_x)
            result = self.simulate_drag(track)
            print(result)

            self.mark_times += 1
            if u'验证通过' in result:
                flag_success = True
            elif u'出现错误:' in result:
                self.browser.execute_script('location.reload()')
            elif u'再' in result:
                time.sleep(4)
                continue
            elif u'吃' in result:
                time.sleep(5)
            else:
                break

        if flag_success:
            time.sleep(random.uniform(1.5, 2))
            # self.browser.execute_script(self.js)
        return True

    def get_image(self, class_name):
        """
        下载并还原极验的验证图
        Args:
            class_name: 验证图所在的html标签的class name
        Returns:
            返回验证图
        Errors:
            IndexError: list index out of range. ajax超时未加载完成，导致image_slices为空
        """
        image_slices = self.browser.find_elements_by_class_name(class_name)
        print(len(image_slices))

        # pdb.set_trace()
        if len(image_slices) == 0:
            print('No such a class')
        div_style = image_slices[0].get_attribute('style')
        # pdb.set_trace()
        image_url = re.findall("background-image: url\(\"(.*)\"\); background-position: (.*)px (.*)px;", div_style)[0][
            0]
        image_url = image_url.replace("webp", "jpg")
        image_filename = parse.urlsplit(image_url).path.split('/')[-1]
        location_list = list()
        for image_slice in image_slices:
            location = dict()
            location['x'] = int(re.findall("background-image: url\(\"(.*)\"\); background-position: (.*)px (.*)px;",
                                           image_slice.get_attribute('style'))[0][1])
            location['y'] = int(re.findall("background-image: url\(\"(.*)\"\); background-position: (.*)px (.*)px;",
                                           image_slice.get_attribute('style'))[0][2])
            location_list.append(location)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
        response = requests.get(image_url, headers=headers, verify=False)

        image = Image.open(BytesIO(response.content))
        image = self.recover_image(image, location_list)
        return image

    def recover_image(self, image, location_list):
        """
        还原验证图像
        Args:
            image: 打乱的验证图像（PIL.Image数据类型）
            location_list: 验证图像每个碎片的位置
        Returns:
           还原过后的图像
        """
        new_im = Image.new('RGB', (260, 116))
        im_list_upper = []
        im_list_down = []
        for location in location_list:
            if location['y'] == -58:
                im_list_upper.append(image.crop((abs(location['x']), 58, abs(location['x']) + 10, 116)))
            if location['y'] == 0:
                im_list_down.append(image.crop((abs(location['x']), 0, abs(location['x']) + 10, 58)))

        x_offset = 0
        for im in im_list_upper:
            new_im.paste(im, (x_offset, 0))
            x_offset += im.size[0]

        x_offset = 0
        for im in im_list_down:
            new_im.paste(im, (x_offset, 58))
            x_offset += im.size[0]

        return new_im

    def get_diff_x(self, image1, image2):
        """
       计算验证图的缺口位置（x轴）
       两张原始图的大小都是相同的260*116，那就通过两个for循环依次对比每个像素点的RGB值，
       如果RGB三元素中有一个相差超过50则就认为找到了缺口的位置
       Args:
           image1: 图像1
           image2: 图像2
       Returns:
           x_offset """
        for x in range(0, 260):
            for y in range(0, 116):
                if not self.__is_similar(image1, image2, x, y):
                    return x

    def __is_similar(self, image1, image2, x_offset, y_offset):
        """
        判断image1, image2的[x, y]这一像素是否相似，如果该像素的RGB值相差都在50以内，则认为相似。
        Args:
            image1: 图像1
            image2: 图像2
            x_offset: x坐标
            y_offset: y坐标
        Returns:
           boolean
        """
        pixel1 = image1.getpixel((x_offset, y_offset))
        pixel2 = image2.getpixel((x_offset, y_offset))
        for i in range(0, 3):
            if abs(pixel1[i] - pixel2[i]) >= 50:
                return False
        return True

    def get_track(self, x_offset):

        track = list()
        length = x_offset - 6
        x = random.randint(1, 5)
        while length - x > 4:
            track.append([x, 0, 0])
            length = length - x
            x = random.randint(1, 5)

        for i in range(length):
            if x_offset > 47:
                track.append([1, 0, random.randint(10, 12) / 100.0])
            else:
                track.append([1, 0, random.randint(13, 14) / 100.0])
        return track

    def simulate_drag(self, track):

        dom_div_slider = self.browser.find_element_by_xpath('//*[@id="gc-box"]/div/div[3]/div[2]')

        ActionChains(self.browser).click_and_hold(on_element=dom_div_slider).perform()

        for x, y, z in track:
            ActionChains(self.browser).move_to_element_with_offset(
                to_element=dom_div_slider,
                xoffset=x + 22,
                yoffset=y + 22).perform()
            time.sleep(z)

        time.sleep(0.9)
        ActionChains(self.browser).release(on_element=dom_div_slider).perform()
        time.sleep(1)
        dom_div_gt_info = self.browser.find_element_by_class_name('gt_info_type')
        return dom_div_gt_info.text
