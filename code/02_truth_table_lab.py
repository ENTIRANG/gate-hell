"""02. 진리표 자동 생성과 제품 테스트

우산 챙김 알림 장치의 판단 규칙을 Python으로 옮기고,
세 입력의 8가지 조합을 모두 시험한다.

    입력  R: 비가 온다 / O: 외출할 예정이다 / U: 우산을 가지고 있다
    출력  A: 알림이 울린다
    판단 규칙  A = R and O and (not U)

실행 방법:
    python 02_truth_table_lab.py
"""

import itertools

INPUT_NAMES = ("R", "O", "U")


# ============================================================
# 판단 함수: 발명품의 판단 회로에 해당한다.
# ============================================================


def decide(rain: bool, going_out: bool, has_umbrella: bool) -> bool:
    """올바른 판단 규칙: 비가 오고, 외출하는데, 우산이 없을 때만 알린다."""
    return rain and going_out and not has_umbrella


def decide_broken_1(rain: bool, going_out: bool, has_umbrella: bool) -> bool:
    """오작동 예 1: and 를 or 로 잘못 쓴 경우."""
    return rain or going_out or not has_umbrella


def decide_broken_2(rain: bool, going_out: bool, has_umbrella: bool) -> bool:
    """오작동 예 2: not 을 빠뜨린 경우."""
    return rain and going_out and has_umbrella


# ============================================================
# 진리표 자동 생성
# ============================================================


def print_truth_table(rule) -> None:
    """세 입력의 모든 조합을 만들어 판단 결과를 0과 1로 출력한다."""
    print("   {}  {}  {} | A".format(*INPUT_NAMES))
    print("  ---------+---")
    for rain, going_out, has_umbrella in itertools.product(
        (False, True), repeat=3
    ):
        answer = rule(rain, going_out, has_umbrella)
        print(
            "   {}  {}  {} | {}".format(
                int(rain), int(going_out), int(has_umbrella), int(answer)
            )
        )


# ============================================================
# 제품 시험표: 종이 진리표에서 예상 출력을 옮겨 적은 것
#   ((비, 외출, 우산), 예상 출력)
# ============================================================

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


def run_tests(rule=decide) -> bool:
    """모든 테스트 사례를 실행하고 통과 여부를 출력한다."""
    passed = 0
    failures = []

    for inputs, expected in TEST_CASES:
        actual = rule(*inputs)
        if actual == expected:
            passed += 1
        else:
            failures.append((inputs, expected, actual))

    total = len(TEST_CASES)
    print("  테스트 결과: {} / {} 통과".format(passed, total))

    for inputs, expected, actual in failures:
        bits = " ".join(str(int(value)) for value in inputs)
        print(
            "  실패 - 입력 ({}) : 예상 {}, 실제 {}".format(
                bits, int(expected), int(actual)
            )
        )

    if not failures:
        print("  모든 입력 조합에서 의도한 대로 작동한다.")
    return not failures


def main() -> None:
    print("=" * 46)
    print("우산 챙김 알림 장치 - 진리표와 테스트")
    print("=" * 46)

    print("[1] 올바른 판단 규칙의 진리표")
    print_truth_table(decide)
    print()

    print("[2] 올바른 판단 규칙의 제품 테스트")
    run_tests(decide)
    print()

    print("[3] 오작동 예 1 (and 대신 or)")
    print_truth_table(decide_broken_1)
    run_tests(decide_broken_1)
    print()

    print("[4] 오작동 예 2 (not 빠뜨림)")
    print_truth_table(decide_broken_2)
    run_tests(decide_broken_2)
    print()

    print("실패한 입력 조합을 자연어 작동 조건과 비교하고,")
    print("어느 연산자를 고쳐야 하는지 설명해 보자.")


if __name__ == "__main__":
    main()
