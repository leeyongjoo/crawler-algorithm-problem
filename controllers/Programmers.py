import requests
import urllib.parse
from bs4 import BeautifulSoup

from modules.user_input import input_login_form


class Programmers(object):
    SITE_NAME = 'programmers'
    SITE_URL = 'https://programmers.co.kr/'
    SITE_LOGIN_FORM = {
        'utf8': '✓',
        'authenticity_token': 'random',
        'user[email]': '',
        'user[password]': '',
    }

    json_data = {
        'login': SITE_LOGIN_FORM,
    }

    def __init__(self):
        """
        0. 세션 생성
        1. 로그인
        2. 언어 설정
        """
        self.sess = requests.Session()

    def __get_programmers_url(self, page_name: str) -> str:
        return urllib.parse.urljoin(self.SITE_URL, f'{page_name}')

    def do_login(self, login_data=None) -> bool:
        """
        로그인

        :return: 정상 동작 여부
        """
        login_url = self.__get_programmers_url('users/login')

        req = self.sess.get(login_url)
        soup = BeautifulSoup(req.text, 'lxml')

        if not login_data:
            login_data: dict = input_login_form(self.SITE_LOGIN_FORM)

        # 매번 인증 토큰이 변경됨
        login_data['authenticity_token'] = soup.select_one('#new_user > input[type=hidden]:nth-child(2)').get('value')

        while True:
            req = self.sess.post(login_url, data=login_data)
            if req.url != login_url:
                print(login_data['user[email]'], '로그인 성공.')
                self.json_data['login'] = login_data
                return True
            else:
                print('아이디나 비밀번호가 잘못되었습니다.')
                login_data: dict = input_login_form(self.SITE_LOGIN_FORM)
