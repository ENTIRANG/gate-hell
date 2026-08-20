"""04. 스마트 발명품 템플릿 (입력 3개 / 출력 1개)

팀 프로젝트용 표준 템플릿이다.
아래 "학생이 수정하는 부분"만 우리 팀 발명품에 맞게 바꾸면
GUI 프레임워크는 그대로 두어도 정상 작동한다.

처음 상태에는 예시로 스마트 복도 절전 조명이 들어 있다.
    입력  P: 사람이 있다 / D: 어둡다 / M: 수동 소등 스위치가 눌렸다
    출력  L: 조명이 켜진다
    판단 규칙  L = P and D and (not M)

실행 방법:
    python 04_invention_starter_1out.py
"""

import itertools
import tkinter as tk
from tkinter import messagebox, ttk

# ============================================================
# 학생이 수정하는 부분
# ============================================================

TITLE = "스마트 복도 절전 조명"
DESCRIPTION = "센서를 켜고 끄면 출력이 즉시 갱신됩니다."

# 가상 센서(입력)의 이름 - 사용자가 뜻을 바로 알 수 있게 쓴다.
INPUT_LABELS = [
    "사람이 있다 (P)",
    "주변이 어둡다 (D)",
    "수동 소등 스위치가 눌렸다 (M)",
]

# 출력 장치의 이름과 상태 문구
OUTPUT_LABEL = "복도 조명"
MESSAGE_ON = "조명을 켭니다."
MESSAGE_OFF = "조명을 끈 상태로 전기를 절약합니다."


def decide(person: bool, dark: bool, manual_off: bool) -> bool:
    """판단 규칙: L = P and D and (not M)"""
    # 매개변수의 개수와 순서는 INPUT_LABELS와 똑같이 맞춘다.
    return person and dark and not manual_off


# 제품 시험표: 종이에 쓴 진리표의 예상 출력을 그대로 옮겨 적는다.
#   ((입력1, 입력2, 입력3), 예상 출력)
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


def all_input_cases():
    """입력 개수에 맞는 모든 조합을 순서대로 만들어 준다."""
    return list(itertools.product((False, True), repeat=INPUT_COUNT))


def check_test_cases() -> str:
    """TEST_CASES의 형식을 검사한다. 문제가 없으면 빈 문자열을 돌려준다."""
    if not TEST_CASES:
        return "TEST_CASES가 비어 있습니다.\n진리표의 예상 출력을 먼저 채우세요."
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
        lines.append("실패한 입력 조합")
        lines.extend(failures)
        lines.append("")
        lines.append("자연어 작동 조건과 논리식을 다시 비교해 보세요.")
    else:
        lines.append("")
        lines.append("모든 입력 조합에서 의도한 대로 작동합니다.")
    return "\n".join(lines)


def open_truth_table(parent) -> None:
    """전체 입력 조합의 예상 출력과 실제 출력을 나란히 보여 주는 창."""
    expected_of = dict(TEST_CASES) if not check_test_cases() else {}

    window = tk.Toplevel(parent)
    window.title("전체 입력 테스트")
    frame = ttk.Frame(window, padding=14)
    frame.pack(fill="both", expand=True)

    headers = ["입력 {}".format(i + 1) for i in range(INPUT_COUNT)]
    headers += ["예상", "실제", "일치"]
    for column, text in enumerate(headers):
        ttk.Label(frame, text=text, font=("TkDefaultFont", 10, "bold")).grid(
            row=0, column=column, padx=6, pady=(0, 6)
        )

    for row, values in enumerate(all_input_cases(), start=1):
        actual = decide(*values)
        expected = expected_of.get(values)
        for column, value in enumerate(values):
            ttk.Label(frame, text=str(int(value))).grid(row=row, column=column)
        ttk.Label(
            frame, text="-" if expected is None else str(int(expected))
        ).grid(row=row, column=INPUT_COUNT)
        ttk.Label(frame, text=str(int(actual))).grid(
            row=row, column=INPUT_COUNT + 1
        )
        if expected is None:
            mark = "?"
        elif expected == actual:
            mark = "O"
        else:
            mark = "X"
        ttk.Label(frame, text=mark).grid(row=row, column=INPUT_COUNT + 2)

    note = "예상 열이 '-'이면 그 조합이 TEST_CASES에 없다는 뜻이다."
    ttk.Label(frame, text=note).grid(
        row=len(all_input_cases()) + 1,
        column=0,
        columnspan=INPUT_COUNT + 3,
        pady=(10, 0),
    )
    ttk.Button(frame, text="닫기", command=window.destroy).grid(
        row=len(all_input_cases()) + 2, column=0, columnspan=INPUT_COUNT + 3,
        pady=(8, 0),
    )


def main() -> None:
    root = tk.Tk()
    root.title(TITLE)

    outer = ttk.Frame(root, padding=16)
    outer.pack(fill="both", expand=True)

    ttk.Label(
        outer, text=TITLE, font=("TkDefaultFont", 14, "bold")
    ).pack(anchor="w")
    ttk.Label(outer, text=DESCRIPTION).pack(anchor="w", pady=(2, 10))

    sensor_box = ttk.LabelFrame(outer, text="가상 센서 입력", padding=10)
    sensor_box.pack(fill="x")

    sensor_vars = [tk.BooleanVar(value=False) for _ in INPUT_LABELS]

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

    button_box = ttk.Frame(outer)
    button_box.pack(fill="x", pady=(12, 0))

    def reset_sensors() -> None:
        for var in sensor_vars:
            var.set(False)
        update_output()

    ttk.Button(button_box, text="초기화", command=reset_sensors).pack(
        side="left"
    )
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
