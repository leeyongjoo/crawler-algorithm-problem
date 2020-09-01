from modules.CodeUp import CodeUp
from modules.FileManager import FileManager
from modules.JsonManager import JsonManager
from modules.user_input import input_index, input_number


def main():
    site_name = 'codeup'

    # json 파일 로드(로그인 정보)
    jm = JsonManager()
    json_data = jm.load_json_file(site_name)

    # CodeUp 객체 생성
    cu = CodeUp(json_data)

    # 로그인 정보 파일로 저장
    if not json_data:
        jm.write_json_file(site_name, cu.json_data)

    # 함수 선택
    # print("<< 함수 선택 >>")
    # functions = [select_problemset, input_problem_number, get_all_problems]
    # for i, func in enumerate(functions):
    #     print(f"{i + 1}. {func.__doc__}")
    # function_idx = input_index('함수를 선택하세요: ', functions) - 1
    # functions[function_idx](cu)

    get_all_problems(cu)

def get_all_problems(cu: CodeUp):
    """모든 문제"""

    print("<< 지금까지 해결한 모든 문제 가져오기(이미 가져온 문제는 제외) >>")

    # TODO: (아이디,제출결과) 쿼리스트링 만들어서 푼 문제 요청하기
    # 제출결과 코드
    # 2: 컴파일중 / 4: 정확한 풀이 / 5: 표현 에러 / 6: 잘못된 풀이 / 7: 시간 초과
    # 8: 메모리 초과 / 9: 출력 한계 초과 / 10: 실행 중 에러 / 11: 컴파일 에러
    # 'https://www.codeup.kr/status.php?&jresult=4&user_id=nyk700'

    cu.json_data['login']['user_id']





def select_problemset(cu: CodeUp):
    """문제집 선택"""

    print("<< 문제집 선택하여 해결한 문제 가져오기 >>")
    # 1. 문제집을 선택해서 해결한 문제 가져오기
    solved_problems, dirname = cu.get_solved_problems_and_dirname_by_selecting_problemset()

    # 2. 가져온 문제들을 문제집 폴더에 각각 파일로 저장
    fm = FileManager(['problemset', dirname])
    for p in solved_problems:
        file_basename = '_'.join([p.id, p.name])
        for i, lang_and_source in enumerate(p.lang_and_source):
            if i > 0:
                fm.write_file(file_basename + f' ({i})', lang_and_source[1], lang_and_source[0])
            else:
                fm.write_file(file_basename, lang_and_source[1], lang_and_source[0])
    print(f"{len(solved_problems)} 개의 문제 저장완료.")


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
        fm = FileManager(['problem_id'])
        file_basename = '_'.join([sp.id, sp.name])
        for i, lang_and_source in enumerate(sp.lang_and_source):
            if i > 0:
                fm.write_file(file_basename + f' ({i})', lang_and_source[1], lang_and_source[0])
            else:
                fm.write_file(file_basename, lang_and_source[1], lang_and_source[0])
        print(f"{sp.id} 번 문제 저장완료.")





if __name__ == "__main__":
    main()
    # print(select_problemset.__doc__)
