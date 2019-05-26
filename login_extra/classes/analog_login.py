import traceback

from settings.conf import *
from settings import plats_conf
from tool.warpper import warning, save_ad_cookies, read_ad_cookies


class AnalogLogin(object):
    def __init__(self,
                 acc=None,
                 acc_xpath=None,
                 pwd=None,
                 pwd_xpath=None,
                 login_url=None,
                 captcha_xpath=None,
                 plat=None,
                 driver='c',
                 login_retry_times=2, *args, **kwargs):
        """
            参数设置
        """
        self.acc = acc
        self.pwd = pwd
        self.acc_xpath = acc_xpath
        self.pwd_xpath = pwd_xpath
        self.login_url = login_url
        self.cap_xpath = captcha_xpath
        self.driver = driver
        self.plat = plat
        self.mark = 0
        self.login_retry_times = login_retry_times
        self.browser = self.choose_browser()
        self.wait = WebDriverWait(self.browser, 10)

    def choose_browser(self):
        """
            浏览器选择
        """
        if self.driver == 'f':
            browser = webdriver.Firefox()
        elif self.driver == 'c':
            chrome_options = webdriver.ChromeOptions()
            # prefs = {"profile.managed_default_content_settings.images": 2}
            # chrome_options.add_experimental_option("prefs", prefs)
            # 设置无头
            # chrome_options.add_argument('headless')
            # chrome_options.add_argument('disable-infobars')
            # chrome_options.add_argument('lang=zh_CN.UTF-8')
            # chrome_options.add_argument(
            #     'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"'
            # )
            browser = webdriver.Chrome(chrome_options=chrome_options)
            browser.set_window_size(1300, 800)
        else:
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36 "
            )
            browser = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'], desired_capabilities=dcap)
            browser.set_window_size(2000, 1000)
        browser.set_page_load_timeout(40)
        return browser

    def wait_el_presence_by_xpath(self, xpath):
        return self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    def get_captcha_text(self):
        """
            验证码处理
        """
        return ''

    def enter(self):
        """
            特定提交方式
        """
        return False

    def __del__(self):
        try:
            self.browser.quit()
        except:
            pass

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
        # 处理数字字母验证码
        if self.cap_xpath:
            cap_el = self.wait_el_presence_by_xpath(self.cap_xpath)
            cap_text = self.get_captcha_text()
            cap_el.send_keys(cap_text)
            end_el = cap_el
        # seld.enter，处理滑动验证码
        if not self.enter():
            end_el.send_keys(Keys.ENTER)

    def to_login(self):
        """
            登录
        """
        print('---plat:{}, user:{}, mark:{}, login_retry_time:{}'.format(self.plat, self.acc, self.mark, self.login_retry_times))
        self.browser.delete_all_cookies()
        self.before_login()
        time.sleep(2)
        self.login()
        time.sleep(2)
        res = self.after_login()
        if res is False and self.mark < self.login_retry_times:
            self.mark += 1
            self.to_login()
        elif self.mark >= self.login_retry_times:
            warning('>>>>login faile, plat:{}, user:{}'.format(self.plat, self.acc))

    def run(self):
        """
            流程
        """
        try:
            if not self.read_browser_cookie():
                time.sleep(1)
                self.to_login()
            time.sleep(1)
            self.save_browser_cookie()
            time.sleep(1)
        except:
            traceback.print_exc()

    def before_login(self):
        """
            跳到登录框
        """
        self.browser.get(self.login_url)

    def after_login(self):
        """
            账号密码输入之后处理
        """
        # 当return False, 会触发重试to_login
        return True

    def read_browser_cookie(self):
        """
            浏览器设置cookie
        """
        self.browser.delete_all_cookies()
        cookies = read_ad_cookies(self.acc, self.plat)
        self.browser.get(self.login_url)
        time.sleep(1)
        for cookie in cookies:
            cookie['domain'] = cookie['domain'] if cookie['domain'].startswith('.') else '.' + cookie['domain']
            self.browser.add_cookie(cookie)
        return self.verify_cookie()

    def verify_cookie(self):
        """
            验证cookie 是否生效
        """

    def save_browser_cookie(self):
        """
            保存最新cookie
        """
        cookies = self.browser.get_cookies()
        save_ad_cookies(self.acc, self.plat, cookies)

    def close(self):
        print('----关闭浏览器')
        self.browser.close()
