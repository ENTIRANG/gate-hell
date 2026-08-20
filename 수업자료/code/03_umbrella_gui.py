"""03. 우산 챙김 알림 장치 (tkinter 공통 실습)

가상 센서 3개(체크박스)의 상태를 판단 함수 decide()에 넣어
출력 장치의 작동 여부를 즉시 보여 주는 디지털 프로토타입이다.

    입력  R: 비가 온다 / O: 외출할 예정이다 / U: 우산을 가지고 있다
    출력  A: 알림이 울린다
    판단 규칙  A = R and O and (not U)

실행 방법:
    python 03_umbrella_gui.py
"""

import itertools
import tkinter as tk
from tkinter import messagebox, ttk

# ============================================================
# 학생이 수정하는 부분
# ============================================================

TITLE = "우산 챙김 알림 장치"
DESCRIPTION = "센서를 켜고 끄면 출력이 즉시 갱신됩니다."

# 가상 센서(입력)의 이름
INPUT_LABELS = [
    "비가 온다 (R)",
    "외출할 예정이다 (O)",
    "우산을 가지고 있다 (U)",
]

# 출력 장치의 이름과 상태 문구
OUTPUT_LABEL = "우산 알림"
MESSAGE_ON = "우산을 챙기세요!"
MESSAGE_OFF = "현재 알림이 필요하지 않습니다."


def decide(rain: bool, going_out: bool, has_umbrella: bool) -> bool:
    """판단 규칙: A = R and O and (not U)"""
    # 비가 오고, 외출할 예정이며, 우산이 없을 때에만 알린다.
    return rain and going_out and not has_umbrella


# 제품 시험표: 종이에 쓴 진리표의 예상 출력을 그대로 옮겨 적는다.
#   ((비, 외출, 우산), 예상 출력)
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
# GUI 프레임워크: 처음에는 수정하지 않음
# ============================================================

INPUT_COUNT = len(INPUT_LABELS)

TEXT_ON = "작동"
TEXT_OFF = "정지"
FG_ON, BG_ON = "#b71c1c", "#ffe0e0"
FG_OFF, BG_OFF = "#1b5e20", "#e3f1e3"


def bits(values) -> str:
    """(True, False, True) 를 '1 0 1' 처럼 0과 1로 나타낸다."""
    return " ".join(str(int(value)) for value in values)


def check_test_cases() -> str:
    """TEST_CASES의 형식을 검사한다. 문제가 없으면 빈 문자열을 돌려준다."""
    if not TEST_CASES:
        return "TEST_CASES가 비어 있습니다.\n진리표의 8가지 경우를 먼저 채우세요."
    for number, case in enumerate(TEST_CASES, start=1):
        if not isinstance(case, tuple) or len(case) != 2:
            return "{}번째 테스트 사례는 ((입력들), 예상출력) 모양이어야 합니다.".format(number)
        inputs, expected = case
        if not isinstance(inputs, tuple) or len(inputs) != INPUT_COUNT:
            return "{}번째 테스트 사례의 입력이 {}개가 아닙니다.".format(
                number, INPUT_COUNT
            )
        if not isinstance(expected, bool):
            return "{}번째 예상 출력은 True 또는 False여야 합니다.".format(number)
    return ""


def run_tests():
    """모든 테스트 사례를 실행하고 (통과 수, 전체 수, 실패 목록)을 돌려준다."""
    passed = 0
    failures = []
    for inputs, expected in TEST_CASES:
        actual = decide(*inputs)
        if actual == expected:
            passed += 1
        else:
            failures.append(
                "입력 ({}) : 예상 {}, 실제 {}".format(
                    bits(inputs), int(expected), int(actual)
                )
            )
    return passed, len(TEST_CASES), failures


def test_report() -> str:
    """전체 테스트 결과를 사람이 읽을 수 있는 문장으로 만든다."""
    problem = check_test_cases()
    if problem:
        return problem

    passed, total, failures = run_tests()
    lines = ["테스트 결과: {} / {} 통과".format(passed, total)]
    if failures:
        lines.append("")
        lines.append("실패한 입력 조합 (R O U 순서)")
        lines.extend(failures)
        lines.append("")
        lines.append("자연어 작동 조건과 논리식을 다시 비교해 보세요.")
    else:
        lines.append("")
        lines.append("모든 입력 조합에서 의도한 대로 작동합니다.")
    return "\n".join(lines)


def print_truth_table() -> None:
    """터미널에 판단 함수의 진리표를 출력한다."""
    print(TITLE, "- 진리표")
    print("   R O U | A")
    print("   ------+--")
    for values in itertools.product((False, True), repeat=INPUT_COUNT):
        print("   {} | {}".format(bits(values), int(decide(*values))))


def main() -> None:
    print_truth_table()

    root = tk.Tk()
    root.title(TITLE)

    outer = ttk.Frame(root, padding=16)
    outer.pack(fill="both", expand=True)

    ttk.Label(
        outer, text=TITLE, font=("TkDefaultFont", 14, "bold")
    ).pack(anchor="w")
    ttk.Label(outer, text=DESCRIPTION).pack(anchor="w", pady=(2, 10))

    # --- 가상 센서 입력 ---
    sensor_box = ttk.LabelFrame(outer, text="가상 센서 입력", padding=10)
    sensor_box.pack(fill="x")

    sensor_vars = [tk.BooleanVar(value=False) for _ in INPUT_LABELS]

    # --- 출력 장치 ---
    output_box = ttk.LabelFrame(outer, text="출력 장치", padding=10)
    output_box.pack(fill="x", pady=(10, 0))

    ttk.Label(output_box, text=OUTPUT_LABEL + " :").grid(
        row=0, column=0, sticky="w"
    )
    state_label = tk.Label(
        output_box, text=TEXT_OFF, width=8, relief="ridge", padx=6, pady=2
    )
    state_label.grid(row=0, column=1, sticky="w", padx=8)
    message_label = ttk.Label(output_box, text=MESSAGE_OFF)
    message_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(8, 0))

    status_label = ttk.Label(outer, text="")

    def update_output(*_args) -> None:
        """센서 상태가 바뀔 때마다 판단 함수를 다시 실행한다."""
        values = [var.get() for var in sensor_vars]
        result = decide(*values)
        state_label.config(
            text=TEXT_ON if result else TEXT_OFF,
            fg=FG_ON if result else FG_OFF,
            bg=BG_ON if result else BG_OFF,
        )
        message_label.config(text=MESSAGE_ON if result else MESSAGE_OFF)
        status_label.config(
            text="입력 {}  ->  출력 {}".format(bits(values), int(result))
        )

    for row, (label, var) in enumerate(zip(INPUT_LABELS, sensor_vars)):
        ttk.Checkbutton(
            sensor_box, text=label, variable=var, command=update_output
        ).grid(row=row, column=0, sticky="w", pady=1)

    # --- 조작 버튼 ---
    button_box = ttk.Frame(outer)
    button_box.pack(fill="x", pady=(12, 0))

    def reset_sensors() -> None:
        for var in sensor_vars:
            var.set(False)
        update_output()

    def show_test_report() -> None:
        messagebox.showinfo("전체 테스트", test_report())

    ttk.Button(button_box, text="초기화", command=reset_sensors).pack(
        side="left"
    )
    ttk.Button(button_box, text="전체 테스트", command=show_test_report).pack(
        side="left", padx=6
    )
    ttk.Button(button_box, text="종료", command=root.destroy).pack(side="right")

    status_label.pack(anchor="w", pady=(10, 0))

    update_output()
    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    main()
