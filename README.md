# codeup-automation
코드업 사이트 알고리즘 문제해결 자동화

> [이전](https://github.com/leeyongjoo/crawler-algorithm-problem#codeup){: target="_blank"}에 로그인을 하여
> 해결한 문제를 가져오기 위해 Selenium을 이용하였음.

속도가 느리다는 단점이 있는 `Selenium` 사용 대신 
`requests` 모듈의 session() 함수를 이용하는 방식으로 속도 개선

## Requirements
- [python](https://www.python.org/downloads/) 3.6 ⬆
- `requests`, `bs4`, `lxml`

필요 모듈 설치 방법:
```shell script
pip install -r requirements.txt
```

## Feature
1. 문제집을 선택하여 **해결한 문제** 가져오기

## Usage

