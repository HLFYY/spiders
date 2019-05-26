import selenium

from classes import analog_login
from settings.conf import *
from tool.YDMHTTPDemo3x import YDMHttp
from tool.warpper import warning
from PIL import Image


class BaiduLogin(analog_login.AnalogLogin):
    verify_cookie_url = 'http://index.baidu.com/v2/main/index.html#/trend/%E4%B9%90%E8%A7%86?words=%E4%B9%90%E8%A7%86'

    def __init__(self, acc, pwd, driver, *args, **kwargs):
        # 'p'
        super(BaiduLogin, self).__init__(captcha_xpath='//input[@name="verifyCode"]', *args, **kwargs)
        # super(BaiduLogin, self).__init__(*args, **kwargs)
        self.acc_xpath = '//input[@name="userName"]'
        self.pwd_xpath = '//input[@name="password"]'
        self.login_url = 'http://index.baidu.com/v2/index.html#/?login=1'
        self.acc = acc
        self.pwd = pwd

    def get_captcha_text(self):
        # element = self.wait_el_presence_by_xpath('//img[@class="pass-verifyCode"]')
        # left = element.location['x']
        # top = element.location['y']
        # right = element.location['x'] + element.size['width']*2
        # bottom = element.location['y'] + element.size['height']*2
        # self.browser.save_screenshot(DIR_ + 'screenshot.png')
        # im = Image.open(DIR_ + 'screenshot.png')
        # im = im.crop((left, top, right, bottom))
        # im.save(DIR_ + '{}_{}.png'.format(self.plat, self.acc))
        # captcha = YDMHttp().run(DIR_ + '{}_{}.png'.format(self.plat, self.acc), codetype=5000)
        # warning('plat:{} || user:{} || captcha: {}'.format(self.plat, self.acc, captcha))
        captcha = input('验证码：')
        return captcha

    def verify_cookie(self):
        self.browser.get(self.verify_cookie_url)
        time.sleep(2)
        return self.verify_cookie_url[7:] in self.browser.current_url

    def after_login(self):
        time.sleep(2)
        self.browser.get(self.verify_cookie_url)
        time.sleep(2)


    def login(self):
        """
            登录账号密码
        """
        acc_el = self.wait_el_presence_by_xpath(self.acc_xpath)
        try:
            acc_el.clear()  # 处理acc残留
        except:
            warning('acc clear error')
        acc_el.send_keys(self.acc)
        time.sleep(1.5)
        pwd_el = self.wait_el_presence_by_xpath(self.pwd_xpath)
        try:
            pwd_el.clear()  # 处理acc残留
        except:
            warning('pwd clear error')
        pwd_el.send_keys(self.pwd)
        end_el = pwd_el
        time.sleep(1.5)

        end_el.send_keys(Keys.ENTER)
        time.sleep(2)
        # 处理数字字母验证码
        if self.cap_xpath:
            try:
                cap_el = self.wait_el_presence_by_xpath(self.cap_xpath)
                cap_text = self.get_captcha_text()
                cap_el.send_keys(cap_text)
                end_el = cap_el
            except selenium.common.exceptions.TimeoutException:
                print('---暂无验证码')
        # seld.enter，处理滑动验证码
        if not self.enter():
            end_el.send_keys(Keys.ENTER)

