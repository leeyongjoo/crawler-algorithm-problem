from typing import List

from controllers.CodeUp import CodeUp
from modules.FileManager import FileManager
from modules.JsonManager import JsonManager
from modules.user_input import input_index

SITE_NAME = 'codeup'


def solved_problem():
    # json 파일 로드(로그인 정보)
    jm = JsonManager()
    json_data = jm.load_json_file(SITE_NAME)

    # codeup 객체 생성
    cu = CodeUp(json_data)

    # 로그인 정보 파일로 저장
    if not json_data:
        jm.write_json_file(SITE_NAME, cu.json_data)

    # 함수 선택
    print("<< 함수 선택 >>")
    functions = [select_problemset, input_problem_number, get_all_problems]
    for i, func in enumerate(functions, start=1):
        print(f"{i}. {func.__doc__}")
    function_idx = input_index('함수를 선택하세요: ', functions)
    functions[function_idx](cu)


def select_problemset(cu: CodeUp):
    """문제집 선택"""

    print("<< 문제집 선택하여 해결한 문제만 가져오기 >>")
    # 1. 문제집을 선택해서 해결한 문제 가져오기
    solved_problems, dirname = cu.get_solved_problems_and_dirname_by_selecting_problemset()

    # 2. 가져온 문제들을 문제집 폴더에 각각 파일로 저장
    fm = FileManager([SITE_NAME, 'problemset', dirname])
    is_success, save_cnt = False, 0
    for j, p in enumerate(solved_problems, start=1):
        file_basename = '_'.join([p.id, p.name])
        for i, lang_and_source in enumerate(p.lang_and_source):
            is_success = fm.write_file(file_basename + (f' ({i})' if i > 0 else ''),
                                       lang_and_source[1], lang_and_source[0])

        if is_success:
            print(f'{file_basename} 저장.')

    print(f"{fm.save_cnt} 개의 문제 저장완료." if fm.save_cnt > 0 else f"이미 저장된 문제집입니다.")


def input_problem_number(cu: CodeUp):
    """문제번호 입력"""

    print("<< 문제번호를 입력하고, 해당 문제 가져오기 >>")
    sp = cu.get_solved_problem_by_number()

    # 예외 1) 해당 문제번호가 없을 경우: name == '해당 문제를 열람할 수 없습니다!!'
    if sp.name == '해당 문제를 열람할 수 없습니다!!':
        print('문제번호가 존재하지 않습니다!')

    # 예외 2) 해당 문제에 해결한 코드가 없을 경우
    elif not sp.lang_and_source:
        print('해결한 코드가 없습니다!')

    # 파일로 저장
    else:
        fm = FileManager([SITE_NAME, 'problem_id'])
        file_basename = '_'.join([sp.id, sp.name])
        for i, lang_and_source in enumerate(sp.lang_and_source):
            if i > 0:
                fm.write_file(file_basename + f' ({i})', lang_and_source[1], lang_and_source[0])
            else:
                fm.write_file(file_basename, lang_and_source[1], lang_and_source[0])
        print(f"{sp.id} 번 문제 저장완료." if fm.save_cnt > 0 else f"이미 저장된 문제입니다.")


def get_all_problems(cu: CodeUp):
    """모든 문제"""
    print("<< 지금까지 해결한 모든 문제 가져오기(이미 가져온 문제는 제외) >>")

    fm = FileManager([SITE_NAME, 'all'])

    # 이미 저장된 파일의 목록 가져오기
    saved_file_list = fm.get_default_dir_file_list()

    # 제외할 problem id 리스트 만들기
    exclude_id_list: List[str] = [file.split('_')[0] for file in saved_file_list]

    # 문제 가져오기
    solved_problems = cu.get_solved_problems_all_not_saved(exclude_id_list)

    # 파일로 저장
    for p in solved_problems:
        file_basename = '_'.join([p.id, p.name])
        for i, lang_and_source in enumerate(p.lang_and_source):
            if i > 0:
                fm.write_file(file_basename + f' ({i})', lang_and_source[1], lang_and_source[0])
            else:
                fm.write_file(file_basename, lang_and_source[1], lang_and_source[0])

    print(f"{fm.save_cnt} 개의 문제 저장완료." if fm.save_cnt > 0 else f"이미 모든 문제를 가져왔습니다.")


if __name__ == "__main__":
    solved_problem()
