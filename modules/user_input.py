from typing import Dict


def input_login_form(before_form: Dict[str, str]) -> Dict[str, str]:
    after_form = {}
    for key in before_form:
        if not before_form[key]:
            after_form[key] = input(f'Input {key}: ')
    return after_form


def input_index(msg: str, check_list: list, minus=False):
    try:
        idx = int(input(msg))
        _ = check_list[idx]
        if not minus and idx < 0:
            print(f'음수입니다!')
            return
    except IndexError:
        print('없는 숫자입니다!')
    except ValueError:
        print('숫자가 아닙니다!')
    else:
        return idx


def input_number(msg: str, minus=False):
    try:
        num = int(input(msg))
        if not minus and num < 0:
            print(f'음수입니다!')
            return
    except ValueError:
        print('숫자가 아닙니다!')
    else:
        return num