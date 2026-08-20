"""[교사용] 우산 챙김 알림 장치 - 학생 수정 영역 정답

04_invention_starter_1out.py 의 "학생이 수정하는 부분"을
우산 챙김 알림 장치로 채운 완성본이다.
아래 블록을 그대로 복사하여 템플릿의 같은 자리에 붙여 넣으면 된다.

이 파일 자체를 실행하면 붙여 넣을 내용이 옳은지 검증한다.

실행 방법:
    python umbrella_solution.py
"""

import itertools

# ============================================================
# 여기부터 템플릿의 "학생이 수정하는 부분"에 붙여 넣는다.
# ============================================================

TITLE = "우산 챙김 알림 장치"
DESCRIPTION = "센서를 켜고 끄면 출력이 즉시 갱신됩니다."

INPUT_LABELS = [
    "비가 온다 (R)",
    "외출할 예정이다 (O)",
    "우산을 가지고 있다 (U)",
]

OUTPUT_LABEL = "우산 알림"
MESSAGE_ON = "우산을 챙기세요!"
MESSAGE_OFF = "현재 알림이 필요하지 않습니다."


def decide(rain: bool, going_out: bool, has_umbrella: bool) -> bool:
    """판단 규칙: A = R and O and (not U)"""
    return rain and going_out and not has_umbrella


TEST_CASES = [
    ((False, False, False), False),
    ((False, False, True), False),
    ((False, True, False), False),
    ((False, True, True), False),
    ((True, False, False), False),
    ((True, False, True), False),
    ((True, True, False), True),
    ((True, True, True), False),
]

# ============================================================
# 붙여 넣을 내용은 여기까지. 아래는 검증용 코드이다.
# ============================================================


def bits(values) -> str:
    return " ".join(str(int(value)) for value in values)


def verify() -> bool:
    """진리표를 출력하고 TEST_CASES와 일치하는지 확인한다."""
    print("   R O U | A")
    print("   ------+--")
    expected_of = dict(TEST_CASES)
    passed = 0
    for values in itertools.product((False, True), repeat=3):
        actual = decide(*values)
        expected = expected_of[values]
        mark = "O" if actual == expected else "X"
        if actual == expected:
            passed += 1
        print("   {} | {}   {}".format(bits(values), int(actual), mark))
    print()
    print("테스트 결과: {} / {} 통과".format(passed, len(TEST_CASES)))
    return passed == len(TEST_CASES)


def main() -> None:
    print("=" * 46)
    print("[정답] " + TITLE)
    print("=" * 46)
    print("출력 장치:", OUTPUT_LABEL)
    print("작동 문구:", MESSAGE_ON)
    print("정지 문구:", MESSAGE_OFF)
    print()
    if verify():
        print("학생 수정 영역이 올바르게 완성되었다.")
    else:
        print("예상 출력과 실제 출력이 다른 행이 있다.")


if __name__ == "__main__":
    main()
