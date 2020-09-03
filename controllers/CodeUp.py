import requests
import urllib.parse
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from modules.user_input import input_login_form, input_index, input_number
from modules.languages import get_languages
from typing import List, Any, Tuple, Text
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
        source = soup.select_one('#source').get_text().replace('\r\n', '\n')
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

    def get_solved_problems_and_dirname_by_selecting_problemset(self) -> Tuple[List[SolvedProblem], str]:
        """문제집 선택해서 해결한 문제만 가져오기"""

        problemsetsol_path = 'problemsetsol.php'

        # 모든 문제집 페이지 GET 요청
        req = self.sess.get(self.__get_codeup_url(problemsetsol_path))
        soup = BeautifulSoup(req.text, 'lxml')
        problemset_tags: ResultSet = soup.select('body > main > div > div > div.col-4 > div > a')[1:]

        # 모든 문제집 목록 출력
        for i, problemset_tag in enumerate(problemset_tags):
            print(f"[{i + 1}] {problemset_tag.get_text()}")

        # 모든 문제집 목록 중 하나 입력
        while True:  # 정상적인 값이 들어올 때 까지 반복
            inputted_idx = input_index('문제집을 선택하세요: ', problemset_tags)
            if inputted_idx:
                break

        selected_problemsetsol_name = problemset_tags[inputted_idx].get_text()
        selected_problemsetsol_href = problemset_tags[inputted_idx].get('href')

        # 선택한 문제집 페이지 GET 요청
        req = self.sess.get(self.__get_codeup_url(selected_problemsetsol_href))
        soup = BeautifulSoup(req.text, 'lxml')

        # 선택한 문제집에서 해결한 문제만 가져오기
        problem_rows: ResultSet = soup.select('#problemset > tbody > tr')
        solved_problems: List[SolvedProblem] = []
        for row in problem_rows:
            success_div: Tag = row.select_one('td:nth-child(1) > div')
            if success_div.text == 'Y':  # 해결한 문제
                p_id = row.select_one('td:nth-child(2) > div').get_text()
                p_name = row.select_one('td:nth-child(3) > div').get_text().strip()

                problem_url = row.find('a').get('href')
                hrefs: List[str] = self.__get_my_source_href(self.__get_codeup_url(problem_url))
                lang_and_source = tuple(self.__get_lang_and_source(self.__get_codeup_url(href)) for href in hrefs)

                solved_problems.append(SolvedProblem(p_id, p_name, lang_and_source))
        return solved_problems, f'[{inputted_idx + 1}] {selected_problemsetsol_name}'

    def get_solved_problem_by_number(self) -> SolvedProblem:
        """문제번호로 해결한 코드 가져오기"""

        problem_path = 'problem.php'
        problem_number = input_number('문제번호를 입력하세요: ')
        qs = urllib.parse.urlencode({'id': problem_number})

        # 문제번호를 쿼리에 넣어서 GET 요청
        problem_url = '?'.join([self.__get_codeup_url(problem_path), qs])
        req = self.sess.get(problem_url)
        soup = BeautifulSoup(req.text, 'lxml')

        hrefs: List[str] = self.__get_my_source_href(problem_url)
        lang_and_source = tuple(self.__get_lang_and_source(self.__get_codeup_url(href)) for href in hrefs)

        p_id = str(problem_number)
        p_name = soup.find('title').get_text().strip()
        return SolvedProblem(p_id, p_name, lang_and_source)

    def get_solved_problems_all_not_saved(self, exclude_id_list: List[str]) -> List[SolvedProblem]:
        """해결한 모든 문제 가져오기"""

        # 'https://www.codeup.kr/status.php?&jresult=4&user_id=아이디'
        status_path = 'status.php'
        qs = urllib.parse.urlencode({'user_id': self.json_data['login']['user_id'],
                                     'jresult': 4})  # 4: 정확한 풀이

        req = self.sess.get('?'.join([self.__get_codeup_url(status_path), qs]))
        soup = BeautifulSoup(req.text, 'lxml')

        problem_rows: ResultSet = soup.select('#result-tab > tbody > tr')
        solved_problems: List[SolvedProblem] = []
        exclude_id_set = set(exclude_id_list)
        prev_href = ''
        while True:
            for row in problem_rows:
                row_a = row.select_one('td:nth-child(3) > div > a:nth-child(1)')
                p_id = row_a.get_text()
                if p_id in exclude_id_set:
                    continue
                p_name = row_a.get('title').strip()

                problem_href = row_a.get('href')
                hrefs: List[str] = self.__get_my_source_href(self.__get_codeup_url(problem_href))
                lang_and_source = tuple(self.__get_lang_and_source(self.__get_codeup_url(href)) for href in hrefs)

                solved_problems.append(SolvedProblem(p_id, p_name, lang_and_source))
                exclude_id_set.add(p_id)

            next_href = soup.select_one('body > main > div > ul > li:nth-child(3) > a').get('href')
            req = self.sess.get(self.__get_codeup_url(next_href))
            soup = BeautifulSoup(req.text, 'lxml')
            problem_rows = soup.select('#result-tab > tbody > tr')
            if prev_href == next_href:
                break
            else:
                prev_href = next_href
        return solved_problems
