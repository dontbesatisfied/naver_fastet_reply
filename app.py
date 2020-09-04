from bs4 import BeautifulSoup
from urllib import request
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import pyperclip
import constant
import datetime


def get_latest_post(blog_id):
    with request.urlopen(
            "https://blog.naver.com/PostList.nhn?blogId={}&categoryNo=0&from=postList".format(blog_id)) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        print(soup.find('h4', {'class': 'category_title pcol2'}).text, datetime.datetime.now())
        return soup.find('h4', {'class': 'category_title pcol2'}).text


class Process:

    def __init__(self):
        self.driver = webdriver.Firefox(executable_path=constant.GECKO_DRIVER_PATH)
        self.driver.implicitly_wait(3)

    def clipboard_input(self, user_xpath, user_input):
        temp_user_input = pyperclip.paste()  # 사용자 클립보드를 따로 저장

        pyperclip.copy(user_input)
        self.driver.find_element_by_xpath(user_xpath).click()
        ActionChains(self.driver).key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform()

        pyperclip.copy(temp_user_input)  # 사용자 클립보드에 저장 된 내용을 다시 가져 옴

    def run(self):
        self.driver.get('https://nid.naver.com/nidlogin.login')
        self.driver.implicitly_wait(1)

        self.clipboard_input('//*[@id="id"]', constant.NAVER_ID)
        self.clipboard_input('//*[@id="pw"]', constant.NAVER_PW)
        self.driver.find_element_by_xpath('//*[@id="log.login"]').click()

        # 초기 값 셋팅
        total_count_text = get_latest_post(constant.BLOG_ID)
        sleep(constant.INTERVAL_SEC)

        while True:
            if constant.MAX_DATETIME < datetime.datetime.now():
                break

            if total_count_text == get_latest_post(constant.BLOG_ID):
                print(constant.INTERVAL_SEC)
                sleep(constant.INTERVAL_SEC)
            else:
                self.driver.get("https://blog.naver.com/PostList.nhn?blogId={}&categoryNo=0&from=postList".format(constant.BLOG_ID))
                reply_button = self.driver.find_element(By.XPATH, "//div[@class='area_comment pcol2']")
                reply_button.click()

                reply_input = self.driver.find_element(By.XPATH, "//div[@class='u_cbox_text u_cbox_text_mention']")
                self.driver.execute_script("arguments[0].innerHTML = arguments[1]", reply_input, constant.REPLY_CONTENT)

                submit_btn = self.driver.find_element(By.XPATH, "//button[@class='u_cbox_btn_upload']")
                submit_btn.click()
                break;
