import urllib.parse
from typing import List
import requests
from modules.JSONManager import JSONManager
from bs4 import BeautifulSoup, ResultSet
from errors import NumNotInRangeError, IdPwNotCorrectError
from modules.user_input import input_login_form, input_index

SITE_NAME = 'codeup'
SITE_URL = 'https://www.codeup.kr/'
SITE_LOGIN_FROM = {
    'user_id': '',
    'password': '',
}


def do_login(sess: requests.Session()) -> bool:
    """
    로그인

    :param sess: 세션
    :return: 정상 동작 여부
    """
    login_url = get_codeup_url('login.php')

    jm = JSONManager(SITE_NAME)
    login_data: dict = jm.load_json_file()
    if not login_data:
        login_data: dict = input_login_form(SITE_LOGIN_FROM)

    while True:
        req = sess.post(login_url, data=login_data)
        if req.text.split('\n')[-2] == 'history.go(-2);':  # -1: 오류, -2: 성공
            print(login_data['user_id'], '로그인 성공.')
            jm.write_json_file(login_data)
            return True
        else:
            print('아이디나 비밀번호가 잘못되었습니다.')
            login_data: dict = input_login_form(SITE_LOGIN_FROM)


def get_codeup_url(page_name: str) -> str:
    return urllib.parse.urljoin(SITE_URL, f'{page_name}')


def get_solved_problem(sess: requests.Session()) -> List:
    problemsetsol_path = 'problemsetsol.php'

    # 모든 문제집 페이지 GET 요청
    req = sess.get(get_codeup_url(problemsetsol_path))
    soup = BeautifulSoup(req.text, 'lxml')
    problemset_tags: ResultSet = soup.select('body > main > div > div > div.col-4 > div > a')
    # 모든 문제집 목록 출력
    for i, problemset_tag in enumerate(problemset_tags):
        print(f"[{i}] {problemset_tag.get_text()}")
    # 모든 문제집 목록 중 하나 입력
    while True:  # 정상적인 값이 들어올 때 까지 반복
        inputted_idx = input_index('문제집 번호를 입력하세요: ', problemset_tags)
        if inputted_idx:
            break

    selected_problemsetsol_href = problemset_tags[inputted_idx].get('href')

    # 선택한 문제집 페이지 GET 요청
    req = sess.get(get_codeup_url(selected_problemsetsol_href))
    soup = BeautifulSoup(req.text, 'lxml')




def main():
    # 0. 세션 생성
    sess = requests.Session()

    # 1. 로그인
    do_login(sess)

    # TODO: 2. 함수 선택

    # 2-1. 해결한 문제 가져오기
    get_solved_problem(sess)


if __name__ == "__main__":
    main()
    pass
