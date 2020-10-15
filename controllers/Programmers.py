from typing import List

import requests
import urllib.parse
from bs4 import BeautifulSoup
from collections import namedtuple

from modules.user_input import input_login_form, input_index
from modules.languages import langs

ToSolveProblem = namedtuple('ToSolveProblem', ['level', 'name', 'content', 'url'])


class Programmers(object):
    SITE_NAME = 'programmers'
    SITE_URL = 'https://programmers.co.kr'
    SITE_LOGIN_FORM = {
        'utf8': '✓',
        'authenticity_token': 'random',
        'user[email]': '',
        'user[password]': '',
    }
    SITE_PROBLEMS_URL = '/'.join([SITE_URL, 'learn', 'challenges'])
    params = {
        'tab': 'all_challenges',
        'page': 1,
    }

    json_data = {
        'login': SITE_LOGIN_FORM,
        'language': '',
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

    def get_to_solve_problem(self, lang):
        to_solve_problems: List[ToSolveProblem] = []
        while True:
            problems_url = '?'.join([self.SITE_PROBLEMS_URL, urllib.parse.urlencode(self.params)])
            html = requests.get(problems_url).text
            soup = BeautifulSoup(html, 'lxml')

            problems = soup.select('#tab_all_challenges > section > div > div.challenge__algorithms--index.col-md-8 '
                                   '> div.algorithm-list > div.row > div')
            if problems:
                print(f"{self.params['page']} 페이지 시작.")
            else:
                break

            for problem in problems:
                # 해당 문제가 지정한 언어를 제공하는 지 검사
                try:
                    problem_path = problem.find('div', {'data-original-title': lang}).find('a').get('href')
                except AttributeError:  # 해당 언어가 없을 경우
                    continue

                problem_level = problem.find('div').get('class')[1].split('-')[1]
                problem_title = problem.find('h4').get_text()
                problem_category = problem.find('h6').get_text()

                problem_url = ''.join([self.SITE_URL, problem_path])
                # language 추가해서 돌림
                file_content = make_file_content(problem_url, lang)
                filename = '[{}] {}'.format(problem_category, problem_title)

                to_solve_problems.append(ToSolveProblem(problem_level, filename, file_content, problem_url))
            self.params['page'] = self.params['page'] + 1
        return to_solve_problems


def select_language():
    print("<< LANGUAGE >>")
    for i, a in enumerate(langs, start=1):
        print(f'[{i}] {a:10s}', end='\t')
        if i % 5 == 0:
            print()
    if len(langs) % 5 != 0:
        print()
    lang_idx = input_index('언어를 선택하세요: ', langs)
    return langs[lang_idx]


def make_file_content(problem_url, lang):
    if lang == 'python3':
        html = requests.get(problem_url).text
        soup = BeautifulSoup(html, 'lxml')

        # <q> 태그를 " 문자로 변환
        for q in soup.findAll('q'):
            text = q.get_text()
            q.replaceWith('"{}"'.format(text))

        # 코드
        code = soup.select_one('#code').get_text()

        # 입출력 예
        p_input_list = []
        p_output_list = []

        p_example_text = soup.find(text='입출력 예')
        p_example_table = None
        if p_example_text is not None:
            p_example_table = p_example_text.find_next('table')

        if p_example_table is None:
            test_code = f'pass'
        else:
            p_example_tr_list = p_example_table.select('tbody > tr')
            p_example_td_list = [e.find_all('td') for e in p_example_tr_list]

            for *i, o in p_example_td_list:
                p_input_list.append([a.get_text() for a in i])
                p_output_list.append(o.get_text())

            # output 중에서 bool 타입은 capitalize
            for i, s in enumerate(p_output_list):
                if s in ['true', 'false']:
                    p_output_list[i] = s.capitalize()

            # 테스트 코드는 마지막 테이블만..
            test_code_list = []
            for i, o in zip(p_input_list, p_output_list):
                test_code_list.append('print(solution({}))'.format(', '.join(i)))
                test_code_list.append('print(solution({}) == {})'.format(', '.join(i), o))
            test_code = f'\n{" " * 4}'.join(test_code_list)

        # 파일 내용
        file_content = f'# {problem_url}\n{code}\n\n\nif __name__ == "__main__":\n{" " * 4}{test_code}\n'
        return file_content


if __name__ == "__main__":
    print(make_file_content('https://programmers.co.kr/learn/courses/30/lessons/67256?language=python3', 'python3'))
    print(make_file_content('https://programmers.co.kr/learn/courses/30/lessons/12925?language=python3', 'python3'))
