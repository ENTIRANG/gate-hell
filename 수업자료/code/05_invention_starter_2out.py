"""05. 스마트 발명품 템플릿 (입력 3개 / 출력 2개)

도전 난이도 팀 프로젝트용 템플릿이다.
판단 함수 decide()는 두 개의 출력을 함께 돌려준다.
두 출력의 목적이 다르면 조건식도 달라져야 한다.

처음 상태에는 예시로 야간 보행 안전등이 들어 있다.
    입력  D: 어둡다 / W: 보행자가 지나간다 / B: 배터리가 부족하다
    출력  L: 안전등이 켜진다,  C: 배터리 경고가 켜진다
    판단 규칙  L = D and W and (not B),   C = B

실행 방법:
    python 05_invention_starter_2out.py
"""

import itertools
import tkinter as tk
from tkinter import messagebox, ttk

# ============================================================
# 학생이 수정하는 부분
# ============================================================

TITLE = "야간 보행 안전등"
DESCRIPTION = "출력 장치마다 작동 조건이 다르다는 점에 주의하세요."

INPUT_LABELS = [
    "주변이 어둡다 (D)",
    "보행자가 지나간다 (W)",
    "배터리가 부족하다 (B)",
]

# 출력 장치 두 개의 이름과 상태 문구 (순서를 맞춘다)
OUTPUT_LABELS = ["보행 안전등", "배터리 경고"]
MESSAGES_ON = [
    "보행자를 위해 안전등을 켭니다.",
    "배터리를 교체하세요.",
]
MESSAGES_OFF = [
    "안전등을 끈 상태로 전력을 절약합니다.",
    "배터리 상태는 정상입니다.",
]


def decide(dark: bool, walking: bool, battery_low: bool):
    """판단 규칙: 두 출력의 목적이 다르므로 조건식도 다르다."""
    # 안전등은 사람이 지나갈 때만 켜서 전력을 절약한다.
    # 배터리 경고는 사람이 없어도 관리자에게 알려야 한다.
    light = dark and walking and not battery_low
    battery_warning = battery_low
    return light, battery_warning


# 제품 시험표: ((입력1, 입력2, 입력3), (예상 출력1, 예상 출력2))
TEST_CASES = [
    ((False, False, False), (False, False)),
    ((False, False, True), (False, True)),
    ((False, True, False), (False, False)),
    ((False, True, True), (False, True)),
    ((True, False, False), (False, False)),
    ((True, False, True), (False, True)),
    ((True, True, False), (True, False)),
    ((True, True, True), (False, True)),
]

# ============================================================
# GUI 프레임워크: 처음에는 수정하지 않음
# ============================================================

INPUT_COUNT = len(INPUT_LABELS)
OUTPUT_COUNT = len(OUTPUT_LABELS)

TEXT_ON = "작동"
TEXT_OFF = "정지"
FG_ON, BG_ON = "#b71c1c", "#ffe0e0"
FG_OFF, BG_OFF = "#1b5e20", "#e3f1e3"


def bits(values) -> str:
    """(True, False) 를 '1 0' 처럼 0과 1로 나타낸다."""
    return " ".join(str(int(value)) for value in values)


def all_input_cases():
    """입력 개수에 맞는 모든 조합을 순서대로 만들어 준다."""
    return list(itertools.product((False, True), repeat=INPUT_COUNT))


def outputs_of(values):
    """decide()의 결과를 항상 길이 2의 튜플로 정리한다."""
    result = decide(*values)
    if not isinstance(result, tuple) or len(result) != OUTPUT_COUNT:
        raise ValueError(
            "decide 함수는 출력 {}개를 튜플로 돌려주어야 합니다.".format(
                OUTPUT_COUNT
            )
        )
    return tuple(bool(item) for item in result)


def check_test_cases() -> str:
    """TEST_CASES의 형식을 검사한다. 문제가 없으면 빈 문자열을 돌려준다."""
    if not TEST_CASES:
        return "TEST_CASES가 비어 있습니다.\n두 출력의 예상값을 먼저 채우세요."
    for number, case in enumerate(TEST_CASES, start=1):
        if not isinstance(case, tuple) or len(case) != 2:
            return "{}번째 테스트 사례는 ((입력들), (예상출력들)) 모양이어야 합니다.".format(
                number
            )
        inputs, expected = case
        if not isinstance(inputs, tuple) or len(inputs) != INPUT_COUNT:
            return "{}번째 테스트 사례의 입력이 {}개가 아닙니다.".format(
                number, INPUT_COUNT
            )
        if not isinstance(expected, tuple) or len(expected) != OUTPUT_COUNT:
            return "{}번째 예상 출력이 {}개가 아닙니다.".format(
                number, OUTPUT_COUNT
            )
    return ""


def run_tests():
    """모든 테스트 사례를 실행하고 (통과 수, 전체 수, 실패 목록)을 돌려준다."""
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


def test_report() -> str:
    """전체 테스트 결과를 사람이 읽을 수 있는 문장으로 만든다."""
    problem = check_test_cases()
    if problem:
        return problem

    try:
        passed, total, failures = run_tests()
    except ValueError as error:
        return str(error)

    lines = ["테스트 결과: {} / {} 통과".format(passed, total)]
    lines.append("출력 순서: {}".format(", ".join(OUTPUT_LABELS)))
    if failures:
        lines.append("")
        lines.append("실패한 입력 조합")
        lines.extend(failures)
        lines.append("")
        lines.append("두 출력의 조건식을 각각 다시 확인해 보세요.")
    else:
        lines.append("")
        lines.append("모든 입력 조합에서 두 출력이 의도한 대로 작동합니다.")
    return "\n".join(lines)


def open_truth_table(parent) -> None:
    """전체 입력 조합에 대한 두 출력의 예상값과 실제값을 보여 주는 창."""
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

    note = "출력 순서: {}".format(", ".join(OUTPUT_LABELS))
    ttk.Label(frame, text=note).grid(
        row=len(cases) + 1, column=0, columnspan=INPUT_COUNT + 3, pady=(10, 0)
    )
    ttk.Button(frame, text="닫기", command=window.destroy).grid(
        row=len(cases) + 2, column=0, columnspan=INPUT_COUNT + 3, pady=(8, 0)
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

    state_labels = []
    message_labels = []
    for index, label in enumerate(OUTPUT_LABELS):
        ttk.Label(output_box, text=label + " :").grid(
            row=index * 2, column=0, sticky="w", pady=(0 if index == 0 else 8, 0)
        )
        chip = tk.Label(
            output_box, text=TEXT_OFF, width=8, relief="ridge", padx=6, pady=2
        )
        chip.grid(
            row=index * 2,
            column=1,
            sticky="w",
            padx=8,
            pady=(0 if index == 0 else 8, 0),
        )
        message = ttk.Label(output_box, text=MESSAGES_OFF[index])
        message.grid(row=index * 2 + 1, column=0, columnspan=2, sticky="w")
        state_labels.append(chip)
        message_labels.append(message)

    status_label = ttk.Label(outer, text="")

    def update_output(*_args) -> None:
        """센서 상태가 바뀔 때마다 두 출력을 함께 갱신한다."""
        values = [var.get() for var in sensor_vars]
        try:
            results = outputs_of(values)
        except ValueError as error:
            status_label.config(text=str(error))
            return
        for index, result in enumerate(results):
            state_labels[index].config(
                text=TEXT_ON if result else TEXT_OFF,
                fg=FG_ON if result else FG_OFF,
                bg=BG_ON if result else BG_OFF,
            )
            message_labels[index].config(
                text=MESSAGES_ON[index] if result else MESSAGES_OFF[index]
            )
        status_label.config(
            text="입력 {}  ->  출력 {}".format(bits(values), bits(results))
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
