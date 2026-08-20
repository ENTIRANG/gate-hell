"""07. 전가산기 프로토타입 템플릿 (B 트랙)

한 자리 이진수 두 개와 아래 자리에서 올라온 올림을 더하는 장치다.

    입력  A, B, Cin
    출력  Sum, Cout
    판단 규칙
        S1   = A xor B
        Sum  = S1 xor Cin
        Cout = (A and B) or (S1 and Cin)

이번 수업에서는 Python의 ^ 연산자를 쓰지 않고,
제1장에서 유도한 대로 and, or, not 으로 xor 를 직접 만든다.

프로그램을 실행하면 여덟 가지 입력 조합의 자동 테스트가 먼저 실행되고,
이어서 프로토타입 창이 열린다.

실행 방법:
    python 07_full_adder_starter.py
"""

import itertools
import tkinter as tk
from tkinter import messagebox, ttk

# ============================================================
# 학생이 수정하는 부분
# ============================================================

TITLE = "한 자리 이진 덧셈기"
DESCRIPTION = "비트를 켜고 끄면 합과 올림이 즉시 갱신됩니다."

INPUT_LABELS = [
    "A = 1",
    "B = 1",
    "Cin = 1  (아래 자리에서 올라온 올림)",
]

OUTPUT_LABELS = ["Sum (합의 자리)", "Cout (올림)"]
MESSAGES_ON = [
    "합의 자리가 1입니다.",
    "윗자리로 1을 올립니다.",
]
MESSAGES_OFF = [
    "합의 자리가 0입니다.",
    "윗자리로 올릴 것이 없습니다.",
]


def xor(a: bool, b: bool) -> bool:
    """XOR: 두 입력이 서로 다를 때만 참"""
    return (a and not b) or (not a and b)


def decide(a: bool, b: bool, carry_in: bool):
    """전가산기: 반가산기 두 개와 OR 하나를 이어 붙인 구조"""
    s1 = xor(a, b)
    digit = xor(s1, carry_in)
    carry_out = (a and b) or (s1 and carry_in)
    return digit, carry_out


# 제품 시험표: ((A, B, Cin), (예상 Sum, 예상 Cout))
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
# GUI 프레임워크: 처음에는 수정하지 않음
# ============================================================

INPUT_COUNT = len(INPUT_LABELS)
OUTPUT_COUNT = len(OUTPUT_LABELS)

TEXT_ON = "1"
TEXT_OFF = "0"
FG_ON, BG_ON = "#0d47a1", "#dde7fb"
FG_OFF, BG_OFF = "#424242", "#eeeeee"


def bits(values) -> str:
    """(True, False) 를 '1 0' 처럼 0과 1로 나타낸다."""
    return " ".join(str(int(value)) for value in values)


def all_input_cases():
    """세 입력의 여덟 가지 조합을 순서대로 만들어 준다."""
    return list(itertools.product((False, True), repeat=INPUT_COUNT))


def outputs_of(values):
    """decide()의 결과를 항상 길이가 2 인 튜플로 정리한다."""
    result = decide(*values)
    if not isinstance(result, tuple) or len(result) != OUTPUT_COUNT:
        raise ValueError(
            "decide 함수는 출력 {} 개를 튜플로 돌려주어야 합니다.".format(
                OUTPUT_COUNT
            )
        )
    return tuple(bool(item) for item in result)


def check_test_cases() -> str:
    """TEST_CASES의 형식을 검사한다. 문제가 없으면 빈 문자열을 돌려준다."""
    if not TEST_CASES:
        return "TEST_CASES 목록이 비어 있습니다.\n진리표의 예상값을 먼저 채우세요."
    for number, case in enumerate(TEST_CASES, start=1):
        if not isinstance(case, tuple) or len(case) != 2:
            return "{} 번째 테스트 사례는 ((입력들), (예상출력들)) 모양이어야 합니다.".format(
                number
            )
        inputs, expected = case
        if not isinstance(inputs, tuple) or len(inputs) != INPUT_COUNT:
            return "{} 번째 테스트 사례의 입력이 {} 개가 아닙니다.".format(
                number, INPUT_COUNT
            )
        if not isinstance(expected, tuple) or len(expected) != OUTPUT_COUNT:
            return "{} 번째 예상 출력이 {} 개가 아닙니다.".format(
                number, OUTPUT_COUNT
            )
    return ""


def run_tests():
    """진리표 비교 테스트. (통과 수, 전체 수, 실패 목록)을 돌려준다."""
    passed = 0
    failures = []
    for inputs, expected in TEST_CASES:
        actual = outputs_of(inputs)
        if tuple(bool(item) for item in expected) == actual:
            passed += 1
        else:
            failures.append(
                "입력 ({}) : 예상 ({}), 실제 ({})".format(
                    bits(inputs), bits(expected), bits(actual)
                )
            )
    return passed, len(TEST_CASES), failures


def run_arithmetic_check():
    """덧셈 검산. A + B + Cin 이 Sum + 2*Cout 과 같은지 확인한다."""
    passed = 0
    failures = []
    for values in all_input_cases():
        digit, carry_out = outputs_of(values)
        left = sum(int(value) for value in values)
        right = int(digit) + 2 * int(carry_out)
        if left == right:
            passed += 1
        else:
            failures.append(
                "입력 ({}) : {} != {} + 2*{}".format(
                    bits(values), left, int(digit), int(carry_out)
                )
            )
    return passed, len(all_input_cases()), failures


def test_report() -> str:
    """두 가지 검사 결과를 사람이 읽을 수 있는 문장으로 만든다."""
    problem = check_test_cases()
    if problem:
        return problem

    try:
        passed, total, failures = run_tests()
        add_passed, add_total, add_failures = run_arithmetic_check()
    except ValueError as error:
        return str(error)

    lines = ["[1] 진리표 비교: {} / {} 통과".format(passed, total)]
    lines.extend(failures)
    lines.append("")
    lines.append(
        "[2] 덧셈 검산 A + B + Cin = Sum + 2*Cout : {} / {} 통과".format(
            add_passed, add_total
        )
    )
    lines.extend(add_failures)
    if not failures and not add_failures:
        lines.append("")
        lines.append("여덟 가지 조합 모두에서 올바르게 덧셈을 수행합니다.")
    return "\n".join(lines)


def print_truth_table_and_tests() -> None:
    """터미널에 진리표와 자동 테스트 결과를 출력한다."""
    print("=" * 52)
    print(TITLE)
    print("=" * 52)
    row = "  {:>2}{:>3}{:>5} |{:>5}{:>6} |{:>9}{:>13}"
    print(row.format("A", "B", "Cin", "Sum", "Cout", "A+B+Cin", "Sum+2*Cout"))
    print("  " + "-" * 12 + "+" + "-" * 11 + "+" + "-" * 22)
    for values in all_input_cases():
        digit, carry_out = outputs_of(values)
        left = sum(int(value) for value in values)
        right = int(digit) + 2 * int(carry_out)
        print(
            row.format(
                int(values[0]), int(values[1]), int(values[2]),
                int(digit), int(carry_out), left, right,
            )
        )
    print()
    for line in test_report().splitlines():
        print("  " + line)
    print("=" * 52)


def open_truth_table(parent) -> None:
    """전체 입력 조합의 예상값과 실제값을 보여 주는 창."""
    expected_of = dict(TEST_CASES) if not check_test_cases() else {}

    window = tk.Toplevel(parent)
    window.title("전체 입력 테스트")
    frame = ttk.Frame(window, padding=14)
    frame.pack(fill="both", expand=True)

    headers = ["A", "B", "Cin", "예상", "실제", "일치"]
    for column, text in enumerate(headers):
        ttk.Label(frame, text=text, font=("TkDefaultFont", 10, "bold")).grid(
            row=0, column=column, padx=7, pady=(0, 6)
        )

    cases = all_input_cases()
    for row, values in enumerate(cases, start=1):
        actual = outputs_of(values)
        expected = expected_of.get(values)
        for column, value in enumerate(values):
            ttk.Label(frame, text=str(int(value))).grid(row=row, column=column)
        ttk.Label(
            frame, text="-" if expected is None else bits(expected)
        ).grid(row=row, column=INPUT_COUNT)
        ttk.Label(frame, text=bits(actual)).grid(
            row=row, column=INPUT_COUNT + 1
        )
        if expected is None:
            mark = "?"
        elif tuple(bool(item) for item in expected) == actual:
            mark = "O"
        else:
            mark = "X"
        ttk.Label(frame, text=mark).grid(row=row, column=INPUT_COUNT + 2)

    note = "예상과 실제 열은 Sum, Cout 순서다."
    ttk.Label(frame, text=note).grid(
        row=len(cases) + 1, column=0, columnspan=INPUT_COUNT + 3, pady=(10, 0)
    )
    ttk.Button(frame, text="닫기", command=window.destroy).grid(
        row=len(cases) + 2, column=0, columnspan=INPUT_COUNT + 3, pady=(8, 0)
    )


def main() -> None:
    print_truth_table_and_tests()

    root = tk.Tk()
    root.title(TITLE)

    outer = ttk.Frame(root, padding=16)
    outer.pack(fill="both", expand=True)

    ttk.Label(
        outer, text=TITLE, font=("TkDefaultFont", 14, "bold")
    ).pack(anchor="w")
    ttk.Label(outer, text=DESCRIPTION).pack(anchor="w", pady=(2, 10))

    input_box = ttk.LabelFrame(outer, text="비트 입력", padding=10)
    input_box.pack(fill="x")

    bit_vars = [tk.BooleanVar(value=False) for _ in INPUT_LABELS]

    output_box = ttk.LabelFrame(outer, text="계산 결과", padding=10)
    output_box.pack(fill="x", pady=(10, 0))

    state_labels = []
    message_labels = []
    for index, label in enumerate(OUTPUT_LABELS):
        top_pad = 0 if index == 0 else 8
        ttk.Label(output_box, text=label + " :").grid(
            row=index * 2, column=0, sticky="w", pady=(top_pad, 0)
        )
        chip = tk.Label(
            output_box, text=TEXT_OFF, width=6, relief="ridge", padx=6, pady=2,
            font=("TkDefaultFont", 12, "bold")
        )
        chip.grid(row=index * 2, column=1, sticky="w", padx=8, pady=(top_pad, 0))
        message = ttk.Label(output_box, text=MESSAGES_OFF[index])
        message.grid(row=index * 2 + 1, column=0, columnspan=2, sticky="w")
        state_labels.append(chip)
        message_labels.append(message)

    sum_label = ttk.Label(outer, text="", font=("TkDefaultFont", 11, "bold"))
    status_label = ttk.Label(outer, text="")

    def update_output(*_args) -> None:
        """비트가 바뀔 때마다 합과 올림을 다시 계산한다."""
        values = [var.get() for var in bit_vars]
        try:
            digit, carry_out = outputs_of(values)
        except ValueError as error:
            status_label.config(text=str(error))
            return
        for index, result in enumerate((digit, carry_out)):
            state_labels[index].config(
                text=TEXT_ON if result else TEXT_OFF,
                fg=FG_ON if result else FG_OFF,
                bg=BG_ON if result else BG_OFF,
            )
            message_labels[index].config(
                text=MESSAGES_ON[index] if result else MESSAGES_OFF[index]
            )
        left = sum(int(value) for value in values)
        sum_label.config(
            text="{} + {} + {} = {}{}  (2)  =  {}".format(
                int(values[0]), int(values[1]), int(values[2]),
                int(carry_out), int(digit), left
            )
        )
        status_label.config(
            text="입력 A B Cin = {}  ->  출력 Sum Cout = {}".format(
                bits(values), bits((digit, carry_out))
            )
        )

    for row, (label, var) in enumerate(zip(INPUT_LABELS, bit_vars)):
        ttk.Checkbutton(
            input_box, text=label, variable=var, command=update_output
        ).grid(row=row, column=0, sticky="w", pady=1)

    sum_label.pack(anchor="w", pady=(10, 0))

    button_box = ttk.Frame(outer)
    button_box.pack(fill="x", pady=(12, 0))

    def reset_bits() -> None:
        for var in bit_vars:
            var.set(False)
        update_output()

    ttk.Button(button_box, text="초기화", command=reset_bits).pack(side="left")
    ttk.Button(
        button_box,
        text="전체 테스트",
        command=lambda: messagebox.showinfo("전체 테스트", test_report()),
    ).pack(side="left", padx=6)
    ttk.Button(
        button_box, text="진리표 보기", command=lambda: open_truth_table(root)
    ).pack(side="left")
    ttk.Button(button_box, text="종료", command=root.destroy).pack(side="right")

    status_label.pack(anchor="w", pady=(10, 0))

    update_output()
    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    main()
