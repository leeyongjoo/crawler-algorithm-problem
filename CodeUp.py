import requests
import urllib.parse
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from modules.user_input import input_login_form, input_index
from modules.languages import get_languages
from typing import List
from collections import namedtuple

SolvedProblem = namedtuple('SolvedProblem', ['id', 'name', 'lang_and_source'])  # lang_and_source는 여러 개
# ToSolveProblem = namedtuple('ToSolveProblem', ['id', 'name', 'input_example', 'output_example'])


class CodeUp(object):
    SITE_NAME = 'codeup'
    SITE_URL = 'https://www.codeup.kr/'
    SITE_LOGIN_FORM = {
        'user_id': '',
        'password': '',
    }

    json_data = {
        'login': SITE_LOGIN_FORM,
        # 'language': ''
    }

    def __init__(self, json_data=None):
        """
        0. 세션 생성
        1. 로그인
        2. 언어 설정
        """
        self.sess = requests.Session()
        if json_data:
            self._do_login(json_data['login'])
            # self._set_language(json_data['language'])
        else:
            self._do_login()
            # self._set_language()

    def __get_codeup_url(self, page_name: str) -> str:
        return urllib.parse.urljoin(self.SITE_URL, f'{page_name}')

    def __get_my_source_href(self, problem_url: str) -> List[str]:
        req = self.sess.get(problem_url)
        soup = BeautifulSoup(req.text, 'lxml')

        # 내 소스(여러개인 것도 있음)
        my_source_a_tags = soup.find_all('a', {'class': 'btn-primary'})
        return [a.get('href') for a in my_source_a_tags]

    def __get_lang_and_source(self, source_url: str):
        req = self.sess.get(source_url)
        soup = BeautifulSoup(req.text, 'lxml')
        lang = soup.select_one('body > main > div > div > '
                               'div.alert.alert-info.mt-1.pb-0 > p').get_text().split(' / ')[2].lower()
        source = soup.select_one('#source').get_text()
        return lang, source

    def _do_login(self, login_data=None) -> bool:
        """
        로그인

        :return: 정상 동작 여부
        """
        if not login_data:
            login_data: dict = input_login_form(self.SITE_LOGIN_FORM)

        login_url = self.__get_codeup_url('login.php')

        while True:
            req = self.sess.post(login_url, data=login_data)
            if req.text.split('\n')[-2] == 'history.go(-2);':  # -1: 오류, -2: 성공
                print(login_data['user_id'], '로그인 성공.')
                self.json_data['login'] = login_data
                return True
            else:
                print('아이디나 비밀번호가 잘못되었습니다.')
                login_data: dict = input_login_form(self.SITE_LOGIN_FORM)

    # def _set_language(self, language=None):
    #     if language:
    #         self.json_data['language'] = language
    #         return
    #
    #     langs = get_languages()
    #     for i, lang in enumerate(langs):
    #         print(f'[{i}] {lang}')
    #     idx = input_index('언어를 선택하세요: ', langs)
    #     self.json_data['language'] = langs[idx]

    def get_solved_problems_by_selecting_problemset(self) -> List[SolvedProblem]:
        # 문제집 선택해서 해결한 문제만 가져오기
        problemsetsol_path = 'problemsetsol.php'

        # 모든 문제집 페이지 GET 요청
        req = self.sess.get(self.__get_codeup_url(problemsetsol_path))
        soup = BeautifulSoup(req.text, 'lxml')
        problemset_tags: ResultSet = soup.select('body > main > div > div > div.col-4 > div > a')

        # 모든 문제집 목록 출력
        for i, problemset_tag in enumerate(problemset_tags):
            print(f"[{i}] {problemset_tag.get_text()}")

        # 모든 문제집 목록 중 하나 입력
        while True:  # 정상적인 값이 들어올 때 까지 반복
            inputted_idx = input_index('문제집을 선택하세요: ', problemset_tags)
            if inputted_idx:
                break

        selected_problemsetsol_href = problemset_tags[inputted_idx].get('href')

        # 선택한 문제집 페이지 GET 요청
        req = self.sess.get(self.__get_codeup_url(selected_problemsetsol_href))
        soup = BeautifulSoup(req.text, 'lxml')

        # 선택한 문제집에서 해결한 문제만 가져오기
        problem_rows: ResultSet = soup.select('#problemset > tbody > tr')
        solved_problems: List[SolvedProblem] = []
        for row in problem_rows[:3]:  # TODO: [:3] 없애기
            success_div: Tag = row.select_one('td:nth-child(1) > div')
            if success_div.text == 'Y':  # 해결한 문제
                hrefs: List[str] = self.__get_my_source_href(self.__get_codeup_url(row.find('a').get('href')))
                lang_and_source = tuple(self.__get_lang_and_source(self.__get_codeup_url(href)) for href in hrefs)

                p_id = row.select_one('td:nth-child(2) > div').get_text()
                p_name = row.select_one('td:nth-child(3) > div').get_text()

                solved_problems.append(SolvedProblem(p_id, p_name, lang_and_source))
        return solved_problems
