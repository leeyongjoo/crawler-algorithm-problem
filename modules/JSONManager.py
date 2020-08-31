"""
json 관리 클래스


"""

from typing import Dict
from pathlib import Path
import os
import json


# 상위 디렉토리 경로
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


class JSONManager(object):
    """
    json 파일을 로드하여 로그인 정보 추출, 반환 메서드 제공
    """
    _JSON_DIR = '_config'  # 파일을 저장할 기본 디렉토리

    def __init__(self, name):
        self.site_name = name
        self.json_dirname = BASE_DIR / self._JSON_DIR
        self.json_basename = ''.join([self.site_name, '.json'])
        self.json_file = self.json_dirname / self.json_basename

    def load_json_file(self) -> json:
        """
        json 파일 로드

        :return: json 파일 객체
        """
        while True:
            try:
                with open(self.json_file) as f:
                    json_data = json.load(f)
            except FileNotFoundError:
                return None
            else:
                return json_data

    def write_json_file(self, form: Dict[str, str]) -> bool:
        """
        json 파일 생성

       :return: bool
        """
        mkdir_if_not_exists(self.json_dirname)
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(form, f, indent=4)
        return True


def mkdir_if_not_exists(path_dir: str):
    while True:
        try:
            if os.path.isdir(path_dir) is False:
                os.mkdir(path_dir)
        except FileNotFoundError:
            print(os.path.abspath(os.path.join(path_dir, os.pardir)))
            mkdir_if_not_exists(
                os.path.abspath(os.path.join(path_dir, os.pardir)))
        else:
            break


if __name__ == "__main__":
    site_name = 'test'
    lm = JSONManager(site_name, ['1','2'])
    print(lm.get_json_data())
