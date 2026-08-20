"""[교사용] 스마트 과학실 안전관리 시스템 - 학생 수정 영역 정답

05_invention_starter_2out.py 의 "학생이 수정하는 부분"을
스마트 과학실 안전관리 시스템으로 채운 완성본이다.
아래 블록을 그대로 복사하여 템플릿의 같은 자리에 붙여 넣으면 된다.

핵심 설계 관점
  경보는 사람에게 위험을 알리는 출력이므로 사람이 있을 때 작동한다.
  환풍기는 위험을 제거하는 출력이므로 사람이 없어도 작동해야 한다.

실행 방법:
    python safety_system_solution.py
"""

import itertools

# ============================================================
# 여기부터 템플릿의 "학생이 수정하는 부분"에 붙여 넣는다.
# ============================================================

TITLE = "스마트 과학실 안전관리 시스템"
DESCRIPTION = "출력 장치마다 작동 조건이 다르다는 점에 주의하세요."

INPUT_LABELS = [
    "가스가 감지되었다 (G)",
    "온도가 지나치게 높다 (H)",
    "실험실 안에 사람이 있다 (P)",
]

OUTPUT_LABELS = ["대피 경보", "환풍기"]
MESSAGES_ON = [
    "즉시 실험실 밖으로 대피하세요!",
    "환풍기를 가동하여 공기를 배출합니다.",
]
MESSAGES_OFF = [
    "대피 경보를 울릴 상황이 아닙니다.",
    "환풍기는 멈춰 있습니다.",
]


def decide(gas: bool, high_temp: bool, person: bool):
    """A = (G or H) and P,   F = G or H"""
    danger = gas or high_temp
    alarm = danger and person
    fan = danger
    return alarm, fan


TEST_CASES = [
    ((False, False, False), (False, False)),
    ((False, False, True), (False, False)),
    ((False, True, False), (False, True)),
    ((False, True, True), (True, True)),
    ((True, False, False), (False, True)),
    ((True, False, True), (True, True)),
    ((True, True, False), (False, True)),
    ((True, True, True), (True, True)),
]

# ============================================================
# 붙여 넣을 내용은 여기까지. 아래는 검증용 코드이다.
# ============================================================


def bits(values) -> str:
    return " ".join(str(int(value)) for value in values)


def verify() -> bool:
    """진리표를 출력하고 TEST_CASES와 일치하는지 확인한다."""
    print("   G H P | A F")
    print("   ------+----")
    expected_of = dict(TEST_CASES)
    passed = 0
    for values in itertools.product((False, True), repeat=3):
        actual = tuple(decide(*values))
        expected = tuple(expected_of[values])
        mark = "O" if actual == expected else "X"
        if actual == expected:
            passed += 1
        print("   {} | {}   {}".format(bits(values), bits(actual), mark))
    print()
    print("테스트 결과: {} / {} 통과".format(passed, len(TEST_CASES)))
    return passed == len(TEST_CASES)


def main() -> None:
    print("=" * 46)
    print("[정답] " + TITLE)
    print("=" * 46)
    print("출력 1:", OUTPUT_LABELS[0], "- 사람이 있을 때만 작동")
    print("출력 2:", OUTPUT_LABELS[1], "- 사람이 없어도 작동")
    print()
    if verify():
        print("두 출력 모두 8가지 조합에서 설계한 대로 작동한다.")
    else:
        print("예상 출력과 실제 출력이 다른 행이 있다.")
    print()
    print("확인 질문: 환풍기 조건을 (G or H) and P 로 바꾸면")
    print("어떤 행이 달라지고, 어떤 위험이 생기는가?")


if __name__ == "__main__":
    main()
