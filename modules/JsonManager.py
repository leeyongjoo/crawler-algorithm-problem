from modules.FileManager import FileManager
from typing import Dict
import json


class JsonManager(FileManager):
    """
    json 파일을 로드하여 로그인 정보 추출, 반환 메서드 제공
    """

    def __init__(self):
        self.default_dir = '_config'
        super().__init__('json')

    def load_json_file(self, name) -> json:
        try:
            with open(self.dirname / ''.join([name, self.extension])) as f:
                json_data = json.load(f)
        except FileNotFoundError:
            return None
        else:
            return json_data

    def write_json_file(self, name, form: Dict[str, str]) -> bool:
        self._mkdir_if_not_exists(self.dirname)
        with open(self.dirname / ''.join([name, self.extension]), 'w', encoding='utf-8') as f:
            json.dump(form, f, indent=4)
        return True


if __name__ == "__main__":
    site_name = 'test'
    jm = JsonManager()
    print(jm.write_json_file(site_name, {'a': '1', 'b': '2'}))
