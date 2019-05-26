from classes import analog_login
from settings.conf import *
from tool.YDMHTTPDemo3x import YDMHttp
from tool.warpper import warning
from PIL import Image


class BaitongLogin(analog_login.AnalogLogin):
    verify_cookie_url = 'http://baitong.baidu.com/#/overview/index/'

    def __init__(self, acc, pwd, driver, *args, **kwargs):
        # 'p'
        super(BaitongLogin, self).__init__(driver=driver, captcha_xpath='//input[@class="check-in fl"]', plat='baitong', *args, **kwargs)
        self.acc_xpath = '//input[@class="com-in user"]'
        self.pwd_xpath = '//input[@class="com-in pass"]'
        self.login_url = 'http://baitong.baidu.com/login.html#/overview/index/'
        self.acc = acc
        self.pwd = pwd

    def get_captcha_text(self):
        element = self.wait_el_presence_by_xpath('//*[@id="img-captcha"]')
        left = element.location['x']
        top = element.location['y']
        right = element.location['x'] + element.size['width']
        bottom = element.location['y'] + element.size['height']
        self.browser.save_screenshot(DIR_ + 'screenshot.png')
        im = Image.open(DIR_ + 'screenshot.png')
        im = im.crop((left, top, right, bottom))
        im.save(DIR_ + 'baitong.png')
        captcha = YDMHttp().run(DIR_ + 'baitong.png')
        warning('baitong || captcha: {}'.format(captcha))
        return captcha


    # def get_captcha_text(self):
    #     time.sleep(1)
    #     cookies = self.browser.get_cookies()
    #     cookie = ''
    #     for d in cookies:
    #         cookie += '{}={};'.format(d['name'], d['value'])
    #     headers = {
    #         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    #         'Cookie': cookie,
    #     }
    #     res = requests.get('https://e.uc.cn/sso/auth.jpg', headers=headers, verify=False)
    #     self.browser.delete_cookie('SsoCaptchaCode')
    #     for c in cookies:
    #         if c['name'] == 'SsoCaptchaCode':
    #             c['value'] = res.cookies['SsoCaptchaCode']
    #         self.browser.add_cookie(c)
    #     file_name = DIR_ + 'uc.png'
    #     with open(file_name, 'wb') as f:
    #         f.write(res.content)
    #     captcha = YDMHttp().run(file_name)
    #     warning('uc|| captcha: {}'.format(captcha))
    #     return captcha

    def before_login(self):
        self.wait_el_presence_by_xpath('//a[@class="to-login"]').click()

    def verify_cookie(self):
        self.browser.get(self.verify_cookie_url)
        time.sleep(2)
        return self.verify_cookie_url[7:] in self.browser.current_url

    def after_login(self):
        time.sleep(2)
        self.browser.get(self.verify_cookie_url)
        time.sleep(2)

