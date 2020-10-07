import os.path

from controllers.Programmers import Programmers, select_language
from modules.FileManager import *
from modules.JsonManager import JsonManager

SITE_NAME = 'programmers'


def to_solve_problem():
    # 해결할 문제 가져오기

    # codeup 객체 생성
    pro = Programmers()

    # 언어 선택
    lang = select_language()

    # 해결할 문제 가져오기
    to_solve_problems = pro.get_to_solve_problem(lang)

    fm = FileManager([SITE_NAME])
    for problem in to_solve_problems:
        filename = remove_win_special_char(problem.name)
        fm.__init__([SITE_NAME, lang, f"level{problem.level}"])
        if fm.write_file(filename, problem.content, lang):
            print(f'level{problem.level}', filename, '저장 완료')

    print(f"{fm.save_cnt} 개의 문제 저장완료." if fm.save_cnt > 0 else f"이미 저장된 문제집입니다.")


def login():
    site_name = 'programmers'

    # json 파일 로드(로그인 정보)
    jm = JsonManager()
    json_data = jm.load_json_file(site_name)

    # Programmers 객체 생성
    p = Programmers()
    if json_data:
        p.do_login(json_data['login'])
    else:
        p.do_login()

    # 로그인 정보 파일로 저장
    if not json_data:
        jm.write_json_file(site_name, p.json_data)


if __name__ == "__main__":
    to_solve_problem()
