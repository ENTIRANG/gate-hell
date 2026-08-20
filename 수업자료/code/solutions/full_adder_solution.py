"""[교사용] 전가산기 정답과 두 자리 덧셈기 확장 예시 (B 트랙)

세 가지를 보여 준다.
  1) 전가산기의 진리표와 두 가지 검증
  2) 흔한 오작동 두 가지와 그 증상
  3) 선택 도전 과제인 두 자리 이진 덧셈기

실행 방법:
    python full_adder_solution.py
"""

import itertools

# ============================================================
# 정답: 07_full_adder_starter.py 의 학생 수정 영역과 같다.
# ============================================================


def xor(a: bool, b: bool) -> bool:
    """XOR: 두 입력이 서로 다를 때만 참"""
    return (a and not b) or (not a and b)


def decide(a: bool, b: bool, carry_in: bool):
    """전가산기: 반가산기 두 개와 OR 하나를 이어 붙인 구조"""
    s1 = xor(a, b)
    digit = xor(s1, carry_in)
    carry_out = (a and b) or (s1 and carry_in)
    return digit, carry_out


TEST_CASES = [
    ((False, False, False), (False, False)),
    ((False, False, True), (True, False)),
    ((False, True, False), (True, False)),
    ((False, True, True), (False, True)),
    ((True, False, False), (True, False)),
    ((True, False, True), (False, True)),
    ((True, True, False), (False, True)),
    ((True, True, True), (True, True)),
]


# ============================================================
# 흔한 오작동
# ============================================================


def decide_broken_1(a: bool, b: bool, carry_in: bool):
    """오작동 예 1: 올림을 OR 가 아니라 AND 로 모은 경우"""
    s1 = xor(a, b)
    digit = xor(s1, carry_in)
    carry_out = (a and b) and (s1 and carry_in)
    return digit, carry_out


def decide_broken_2(a: bool, b: bool, carry_in: bool):
    """오작동 예 2: 두 번째 반가산기에서 Cin 을 빠뜨린 경우"""
    s1 = xor(a, b)
    digit = s1
    carry_out = (a and b) or (s1 and carry_in)
    return digit, carry_out


# ============================================================
# 검증
# ============================================================


def bits(values) -> str:
    return " ".join(str(int(value)) for value in values)


def all_cases():
    return list(itertools.product((False, True), repeat=3))


def verify(rule) -> bool:
    """진리표 비교와 덧셈 검산을 함께 수행한다."""
    expected_of = dict(TEST_CASES)
    table_ok = 0
    add_ok = 0
    row = "  {:>2}{:>3}{:>5} |{:>5}{:>6} |{:>7}{:>7}"
    print(row.format("A", "B", "Cin", "Sum", "Cout", "table", "add"))
    print("  " + "-" * 12 + "+" + "-" * 11 + "+" + "-" * 14)
    for values in all_cases():
        digit, carry_out = rule(*values)
        expected = expected_of[values]
        same = (bool(digit), bool(carry_out)) == expected
        left = sum(int(value) for value in values)
        right = int(digit) + 2 * int(carry_out)
        adds = left == right
        table_ok += int(same)
        add_ok += int(adds)
        print(
            row.format(
                int(values[0]), int(values[1]), int(values[2]),
                int(digit), int(carry_out),
                "O" if same else "X", "O" if adds else "X",
            )
        )
    print()
    print("  진리표 비교: {} / 8 통과".format(table_ok))
    print("  덧셈 검산  : {} / 8 통과".format(add_ok))
    return table_ok == 8 and add_ok == 8


# ============================================================
# 선택 도전: 두 자리 이진 덧셈기
#   오른쪽 자리의 Cout 을 왼쪽 자리의 Cin 으로 연결한다.
# ============================================================


def add_two_bits(a1: bool, a0: bool, b1: bool, b0: bool):
    """두 자리 이진수 (a1 a0) 와 (b1 b0) 를 더한다."""
    digit0, carry0 = decide(a0, b0, False)
    digit1, carry1 = decide(a1, b1, carry0)
    return carry1, digit1, digit0


def show_two_bit_adder() -> None:
    row = "  {:>5}{:>6} |{:>7} |{:>6}{:>5}{:>5}"
    print(row.format("A", "B", "A+B", "left", "right", "ok"))
    print("  " + "-" * 12 + "+" + "-" * 8 + "+" + "-" * 16)
    for a1, a0, b1, b0 in itertools.product((False, True), repeat=4):
        c, d1, d0 = add_two_bits(a1, a0, b1, b0)
        left = (int(a1) * 2 + int(a0)) + (int(b1) * 2 + int(b0))
        right = int(c) * 4 + int(d1) * 2 + int(d0)
        print(
            row.format(
                "{}{}".format(int(a1), int(a0)),
                "{}{}".format(int(b1), int(b0)),
                "{}{}{}".format(int(c), int(d1), int(d0)),
                left, right, "O" if left == right else "X",
            )
        )


def main() -> None:
    print("=" * 52)
    print("[정답] 전가산기")
    print("=" * 52)
    print("Sum  = A xor B xor Cin")
    print("Cout = (A and B) or ((A xor B) and Cin)")
    print()

    print("[1] 정답 판단 함수")
    if verify(decide):
        print("  두 검사 모두 통과했다.")
    print()

    print("[2] 오작동 예 1: 올림을 OR 대신 AND 로 모은 경우")
    verify(decide_broken_1)
    print("  진단: 두 반가산기에서 동시에 올림이 나는 일은 없으므로")
    print("        AND 로 모으면 Cout 이 항상 0 이 된다. OR 로 고친다.")
    print()

    print("[3] 오작동 예 2: 두 번째 반가산기에서 Cin 을 빠뜨린 경우")
    verify(decide_broken_2)
    print("  진단: Cin 이 1 인 행에서 Sum 이 틀린다.")
    print("        digit = xor(s1, carry_in) 으로 고친다.")
    print()

    print("[4] 선택 도전: 두 자리 이진 덧셈기")
    print("  오른쪽 자리의 Cout 을 왼쪽 자리의 Cin 으로 연결하면 된다.")
    show_two_bit_adder()


if __name__ == "__main__":
    main()
