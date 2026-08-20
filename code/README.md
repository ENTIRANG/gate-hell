# 조건을 설계하라 — Python 실습 파일

「불 대수와 논리게이트로 만드는 스마트 발명품」 2일차 실습에 사용하는
Python 파일 모음이다. 모두 Python 표준 라이브러리만 사용한다.

## 1. 준비

터미널(명령 프롬프트)에서 다음을 확인한다.

```
python --version
python -m tkinter
```

`python` 명령이 인식되지 않으면 Windows에서는 `py`를 사용한다.

```
py --version
py -m tkinter
```

작은 tkinter 창이 열리면 준비가 끝난 것이다.
설치해야 하는 외부 패키지는 없다. `pip install`은 필요하지 않다.

Python 편집기는 제한하지 않는다. IDLE, VS Code, 그 밖의 편집기 중
편한 것을 사용하면 된다. 파일을 저장한 뒤 실행해야 수정 내용이 반영된다.

## 2. 파일의 역할

| 파일 | 성격 | 역할 |
|---|---|---|
| `00_environment_check.py` | 실행 | Python 버전과 tkinter 동작 확인 |
| `01_boolean_practice.py` | 실행·수정 | `True/False`, `and/or/not`, 2입력 진리표 |
| `02_truth_table_lab.py` | 실행·수정 | 진리표 자동 생성, `TEST_CASES`, 오작동 진단 |
| `03_umbrella_gui.py` | 실행·수정 | 공통 실습: 우산 챙김 알림 장치 (입력 3 / 출력 1) |
| `04_invention_starter_1out.py` | 팀 프로젝트 | 표준 난이도 템플릿 (입력 3 / 출력 1) |
| `05_invention_starter_2out.py` | 팀 프로젝트 | 도전 난이도 템플릿 (입력 3 / 출력 2) |
| `06_safety_system_example.py` | 참고 | 완성 예시: 스마트 과학실 안전관리 시스템 |
| `07_full_adder_starter.py` | 팀 프로젝트 | B 트랙 템플릿: 전가산기 (입력 3 / 출력 2) |
| `solutions/` | 교사용 | 정답과 검증 스크립트 |

## 3. 실행 방법

파일이 있는 폴더에서 다음과 같이 실행한다.

```
python 03_umbrella_gui.py
```

`00`~`02`는 터미널에 결과를 출력하는 프로그램이고,
`03`~`07`은 창이 열리는 프로그램이다.
창이 열리는 프로그램도 실행하는 동안 터미널에 진리표를 함께 출력한다.

## 4. 학생이 수정하는 파일

A 트랙 팀은 `04_invention_starter_1out.py` 또는
`05_invention_starter_2out.py`를, B 트랙 팀은 `07_full_adder_starter.py`를
팀 폴더에 복사한 뒤 수정한다.

각 파일은 두 영역으로 나뉘어 있다.

```
# ============================================================
# 학생이 수정하는 부분
# ============================================================
```

- `TITLE`, `DESCRIPTION` : 장치 이름과 한 줄 설명
- `INPUT_LABELS` : 가상 센서(B 트랙은 비트)의 이름
- `OUTPUT_LABEL` / `OUTPUT_LABELS` : 출력 장치(B 트랙은 Sum, Cout)의 이름
- `MESSAGE_ON` / `MESSAGE_OFF` : 작동·정지 상태 문구
- `decide()` : 판단 규칙(논리식)
- `TEST_CASES` : 진리표에서 옮겨 적은 제품 시험표

```
# ============================================================
# GUI 프레임워크: 처음에는 수정하지 않음
# ============================================================
```

창 생성, 체크박스 생성, 버튼, 배치, 결과 갱신, 테스트 실행은
이 영역이 담당한다. 기본 과제에서는 손대지 않아도 된다.

`INPUT_LABELS`의 개수와 `decide()`의 매개변수 개수, `TEST_CASES`의
입력 개수는 반드시 같아야 한다.

## 5. 자주 발생하는 오류

| 증상 | 원인 | 해결 |
|---|---|---|
| `python: command not found` | 명령 이름이 다름 | `py`로 실행 |
| `ModuleNotFoundError: No module named 'tkinter'` | tkinter 미포함 배포판 | python.org 배포판으로 재설치 |
| `IndentationError` | 들여쓰기가 어긋남 | `return` 앞을 공백 4칸으로 맞춤 |
| `TypeError: decide() takes 3 positional arguments but 4 were given` | 센서 개수와 매개변수 개수가 다름 | `INPUT_LABELS`와 `decide()`의 개수를 맞춤 |
| `SyntaxError: invalid syntax` | 따옴표·괄호·콜론 누락 | 오류 줄 번호의 앞뒤를 확인 |
| 수정했는데 결과가 그대로 | 저장하지 않음 | 저장 후 다시 실행 |
| 창이 열리지 않음 | 다른 창 뒤에 가려짐 | 작업 표시줄 확인, `python -m tkinter`로 재확인 |
| 테스트 결과가 이상함 | `TEST_CASES` 형식 오류 | 안내 메시지의 번호에 해당하는 줄을 수정 |

`&`, `|`, `~`, `^`는 비트 연산자이므로 이번 수업에서는 사용하지 않는다.
논리 연산에는 반드시 `and`, `or`, `not`을 사용한다.
XOR가 필요하면 이 세 연산으로 직접 만든다.

## 6. 파일 저장

- 인코딩은 UTF-8로 저장한다. 대부분의 편집기가 기본값이다.
- 파일 이름은 영문과 숫자로 짓는다. 팀 파일은
  `team03_invention.py`처럼 팀 번호를 앞에 붙인다.
- 원본 템플릿은 그대로 두고 복사본을 수정한다.
