"""01. 불 대수를 Python으로 옮기기

수학 기호와 Python 연산자의 대응을 직접 확인하는 콘솔 실습이다.

    논리곱 (and) : P and Q
    논리합 (or)  : P or Q
    부정   (not) : not P

실행 방법:
    python 01_boolean_practice.py
"""


def show_two_values() -> None:
    """불 변수가 가질 수 있는 두 값을 확인한다."""
    print("[1] 불 변수의 두 값")
    print("  True  =", True, " / 정수로 보면", int(True))
    print("  False =", False, "/ 정수로 보면", int(False))
    print("  0은 거짓, 감지되지 않음, 꺼짐")
    print("  1은 참,   감지됨,       켜짐")
    print()


def show_operators() -> None:
    """세 가지 기본 연산을 하나씩 확인한다."""
    print("[2] 세 가지 기본 연산")
    print("  True  and False =", True and False)
    print("  True  or  False =", True or False)
    print("  not True        =", not True)
    print("  not False       =", not False)
    print()


def show_truth_table() -> None:
    """두 입력에 대한 진리표를 0과 1로 출력한다."""
    print("[3] 두 입력 진리표")
    print("   P  Q | not P | P and Q | P or Q")
    print("  ------+-------+---------+-------")
    for p in (False, True):
        for q in (False, True):
            print(
                "   {}  {} |   {}   |    {}    |   {}".format(
                    int(p),
                    int(q),
                    int(not p),
                    int(p and q),
                    int(p or q),
                )
            )
    print()


# ============================================================
# 실험 구역: 아래 값을 바꾸어 결과를 예측하고 확인해 보자.
# ============================================================

# 스마트 복도 조명: L = P and D
person_here = True      # P: 사람이 있다
is_dark = False         # D: 어둡다


def hallway_light(person: bool, dark: bool) -> bool:
    """복도 조명의 판단 규칙: 사람이 있고 어두울 때만 켠다."""
    return person and dark


def show_experiment() -> None:
    """실험 구역의 값으로 조명 작동 여부를 확인한다."""
    print("[4] 실험: 스마트 복도 조명")
    print("  P(사람) =", int(person_here), " D(어둠) =", int(is_dark))
    result = hallway_light(person_here, is_dark)
    print("  L = P and D =", int(result))
    if result:
        print("  -> 조명을 켠다.")
    else:
        print("  -> 조명을 켜지 않는다.")
    print()
    print("  person_here와 is_dark의 값을 바꾸어 네 가지 경우를 모두")
    print("  확인하고, 종이에 쓴 진리표와 같은지 비교해 보자.")


def main() -> None:
    print("=" * 46)
    print("불 대수 Python 실습")
    print("=" * 46)
    show_two_values()
    show_operators()
    show_truth_table()
    show_experiment()


if __name__ == "__main__":
    main()
