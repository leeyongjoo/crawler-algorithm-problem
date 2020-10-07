# crawler-algorithm-problem
알고리즘 문제해결 사이트(`Programmers`, `CodeUp`) 자동화

## Requirements
- [python](https://www.python.org/downloads/) 3.6 ⬆
- `requests`, `bs4`, `lxml`

필요 모듈 설치 방법:
```shell script
pip install -r requirements.txt
```

## Usage
```shell script
python -m programmers 또는 python -m codeup
```

## Structure
```shell script
crawler-algorithm-problem
│
├─ apps
│  ├─ codeup            : solved_problem.py / submit.py(예정)
│  └─ programmers       : to_solved_problem.py
│  
├─ controllers		: 각 사이트에 대한 컨트롤러 클래스
│ 
├─ modules              : 파일 처리, 언어 선택, 사용자 입력 관련 모듈
│ 
├─ _downloads           : 가져온 문제 파일 디렉토리()
│  │
│  ├─ codeup
│  │  ├─ all            : 모든 문제
│  │  ├─ problemset     : 선택한 문제집
│  │  └─ problem_id     : 입력한 문제번호
│  │
│  └─ programmers
│      └─ python3       : 선택한 언어
│          ├─ level1
│          ├─ level2
│          ├─ level3
│          ├─ level4
│          └─ level5
└─ _jsons               : 로그인 정보 등 기본값 설정 파일
```

## Feature
알고리즘 문제해결 사이트에서 **해결할 문제의 양식**

또는 앞으로 **해결한 문제의 제출 코드**을 가져와서 파일로 저장 


### Programmers
[`to_solved_problem.py`](https://github.com/leeyongjoo/crawler-algorithm-problem/blob/master/apps/programmers/to_solved_problem.py)
- 언어 선택
- 선택한 언어에 대한 모든 문제 크롤링


### CodeUp
> [이전](https://github.com/leeyongjoo/crawler-algorithm-problem-old#codeup) 방식은 `Selenium`을 이용하였음.   
> 속도가 느리다는 단점이 있는 `Selenium` 사용 대신   
> `requests` 모듈의 `session()` 함수를 이용하여 로그인 세션을 얻는 방식으로 속도 개선

[`solved_problem.py`](https://github.com/leeyongjoo/codeup-automation/blob/master/apps/codeup/solved_problem.py)
- 사이트 로그인
- 3 가지 방식의 함수 구현   
  1. 문제집 선택 -> 선택한 문제집에서 해결한 문제의 제출 코드 가져오기
  2. 문제번호 입력 -> 입력한 문제의 제출 코드 가져오기
  3. 해결한 모든 문제 가져오기(이미 저장되어 있는 문제는 제외)
- 가져온 파일로 저장

