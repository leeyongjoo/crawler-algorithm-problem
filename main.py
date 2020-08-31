from CodeUp import CodeUp
from modules.FileManager import FileManager
from modules.JsonManager import JsonManager


# TODO: (아이디,제출결과) 쿼리스트링 만들어서 푼 문제 요청하기
# 제출결과 코드
# 2: 컴파일중 / 4: 정확한 풀이 / 5: 표현 에러 / 6: 잘못된 풀이 / 7: 시간 초과
# 8: 메모리 초과 / 9: 출력 한계 초과 / 10: 실행 중 에러 / 11: 컴파일 에러
# 'https://www.codeup.kr/status.php?&jresult=4&user_id=nyk700'

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

    # TODO: 함수 선택

    # 1-1. 문제집을 선택해서 해결한 문제 가져오기
    print('<< 문제집을 선택하여 해결한 문제 가져오기 >>')
    index_and_problemsetsol_name, solved_problems = cu.get_solved_problems_by_selecting_problemset()

    # 1-2. 가져온 문제들을 문제집 폴더에 각각 파일로 저장
    fm = FileManager(index_and_problemsetsol_name)
    for p in solved_problems:
        file_basename = '_'.join([p.id, p.name])
        for i, lang_and_source in enumerate(p.lang_and_source):
            if i > 0:
                file_basename = ''.join([file_basename, f' ({i})'])
            fm.write_file(file_basename, lang_and_source[1], lang_and_source[0])

    # 2. 문제 번호를 입력하여 가져오기


if __name__ == "__main__":
    main()
