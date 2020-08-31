from pathlib import Path
from modules.languages import get_extension
import os.path

# 상위 디렉토리 경로
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


class FileManager(object):
    default_dir = 'files'  # 파일을 저장할 기본 디렉토리

    def __init__(self):
        self.dirname = BASE_DIR / self.default_dir

    def write_file(self, name, content, language) -> bool:
        mkdir_if_not_exists(self.dirname)
        with open(self.dirname / ''.join([name, get_extension(language)]), 'w', encoding='utf-8') as f:
            f.write(content)
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
            return