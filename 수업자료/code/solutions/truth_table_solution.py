"""[교사용] 02_truth_table_lab.py 정답 및 오류 수정 해설

세 가지를 함께 보여 준다.
  1) 우산 챙김 알림 장치의 완성된 진리표
  2) 완성된 TEST_CASES와 8/8 통과 결과
  3) 오작동 판단 함수가 어느 행에서 왜 실패하는지

실행 방법:
    python truth_table_solution.py
"""

import itertools

HEADER = "   R O U | A"
RULE_LINE = "   ------+--"


def decide(rain: bool, going_out: bool, has_umbrella: bool) -> bool:
    """정답: A = R and O and (not U)"""
    return rain and going_out and not has_umbrella


def decide_broken_1(rain: bool, going_out: bool, has_umbrella: bool) -> bool:
    """오작동 예 1: and 를 or 로 잘못 쓴 경우."""
    return rain or going_out or not has_umbrella


def decide_broken_2(rain: bool, going_out: bool, has_umbrella: bool) -> bool:
    """오작동 예 2: not 을 빠뜨린 경우."""
    return rain and going_out and has_umbrella


# 정답 진리표를 그대로 옮긴 제품 시험표
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

# 실패 행마다 학생에게 설명해 줄 이유
REASONS = {
    (False, False, False): "비도 오지 않고 외출도 하지 않는데 경고한다.",
    (False, True, False): "비가 오지 않는데 경고한다.",
    (False, True, True): "비가 오지 않는데 경고한다.",
    (True, False, False): "외출하지 않는데 경고한다.",
    (True, False, True): "외출하지 않는데 경고한다.",
    (True, True, True): "이미 우산을 가지고 있는데 경고한다.",
    (True, True, False): "정말 필요한 상황인데 경고하지 않는다.",
}


def bits(values) -> str:
    return " ".join(str(int(value)) for value in values)


def print_truth_table(rule) -> None:
    print(HEADER)
    print(RULE_LINE)
    for values in itertools.product((False, True), repeat=3):
        print("   {} | {}".format(bits(values), int(rule(*values))))


def run_tests(rule) -> bool:
    passed = 0
    failures = []
    for inputs, expected in TEST_CASES:
        actual = rule(*inputs)
        if actual == expected:
            passed += 1
        else:
            failures.append((inputs, expected, actual))

    print("  테스트 결과: {} / {} 통과".format(passed, len(TEST_CASES)))
    for inputs, expected, actual in failures:
        print(
            "  실패 - 입력 ({}) : 예상 {}, 실제 {}  <- {}".format(
                bits(inputs),
                int(expected),
                int(actual),
                REASONS.get(inputs, "작동 조건과 다르다."),
            )
        )
    if not failures:
        print("  모든 입력 조합에서 의도한 대로 작동한다.")
    return not failures


def main() -> None:
    print("=" * 56)
    print("[정답] 우산 챙김 알림 장치")
    print("=" * 56)
    print("A = R and O and (not U)")
    print()

    print("[1] 정답 진리표")
    print_truth_table(decide)
    print()
    print("[2] 정답 판단 함수의 테스트")
    run_tests(decide)
    print()

    print("[3] 오작동 예 1 (and 대신 or) - 6개 행에서 실패")
    run_tests(decide_broken_1)
    print("  진단: or 는 조건 중 하나만 참이어도 작동하므로")
    print("        불필요한 경고가 매우 많아진다. and 로 고친다.")
    print()

    print("[4] 오작동 예 2 (not 빠뜨림) - 2개 행에서 실패")
    run_tests(decide_broken_2)
    print("  진단: 우산을 이미 가진 경우에 경고하고,")
    print("        정말 필요한 경우에는 침묵한다. not U 로 고친다.")


if __name__ == "__main__":
    main()
