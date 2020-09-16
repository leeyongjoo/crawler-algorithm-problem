from controllers.Programmers import Programmers
from modules.FileManager import FileManager
from modules.JsonManager import JsonManager

def main():
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
    main()