"""06. 스마트 과학실 안전관리 시스템 (완성 예시)

하나의 센서 묶음으로 두 개의 출력 장치를 제어하는 예시다.
출력의 목적이 다르면 조건식도 달라진다는 점이 이 예시의 핵심이다.

    입력  G: 가스가 감지되었다 / H: 온도가 지나치게 높다 / P: 사람이 있다
    출력  A: 대피 경보가 울린다,  F: 환풍기가 작동한다
    판단 규칙
        danger = G or H
        A = danger and P     (경보는 사람에게 알리는 출력)
        F = danger           (환풍기는 위험을 제거하는 출력)

프로그램을 실행하면 8가지 입력 조합의 자동 테스트가 먼저 실행되고,
이어서 프로토타입 창이 열린다.

실행 방법:
    python 06_safety_system_example.py
"""

import itertools
import tkinter as tk
from tkinter import messagebox, ttk

TITLE = "스마트 과학실 안전관리 시스템"
DESCRIPTION = "센서를 켜고 끄면 두 출력 장치의 상태가 즉시 갱신됩니다."

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
    """두 출력의 목적이 다르므로 조건식도 다르다."""
    danger = gas or high_temp
    alarm = danger and person
    fan = danger
    return alarm, fan


# 제품 시험표: ((G, H, P), (예상 A, 예상 F))
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

INPUT_COUNT = len(INPUT_LABELS)
OUTPUT_COUNT = len(OUTPUT_LABELS)

TEXT_ON = "작동"
TEXT_OFF = "정지"
FG_ON, BG_ON = "#b71c1c", "#ffe0e0"
FG_OFF, BG_OFF = "#1b5e20", "#e3f1e3"

LEVEL_DANGER = ("위험", "#b71c1c")
LEVEL_CAUTION = ("주의", "#ef6c00")
LEVEL_NORMAL = ("정상", "#1b5e20")


def bits(values) -> str:
    """(True, False) 를 '1 0' 처럼 0과 1로 나타낸다."""
    return " ".join(str(int(value)) for value in values)


def all_input_cases():
    """세 입력의 8가지 조합을 순서대로 만들어 준다."""
    return list(itertools.product((False, True), repeat=INPUT_COUNT))


def safety_level(alarm: bool, fan: bool):
    """사용자에게 보여 줄 상태 등급을 정한다."""
    if alarm:
        return LEVEL_DANGER
    if fan:
        return LEVEL_CAUTION
    return LEVEL_NORMAL


def run_tests():
    """모든 테스트 사례를 실행하고 (통과 수, 전체 수, 실패 목록)을 돌려준다."""
    passed = 0
    failures = []
    for inputs, expected in TEST_CASES:
        actual = decide(*inputs)
        if tuple(expected) == tuple(actual):
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
    passed, total, failures = run_tests()
    lines = ["테스트 결과: {} / {} 통과".format(passed, total)]
    lines.append("출력 순서: {}".format(", ".join(OUTPUT_LABELS)))
    if failures:
        lines.append("")
        lines.append("실패한 입력 조합")
        lines.extend(failures)
    else:
        lines.append("")
        lines.append("8가지 입력 조합 모두 설계한 대로 작동합니다.")
    return "\n".join(lines)


def print_truth_table_and_tests() -> None:
    """터미널에 진리표와 자동 테스트 결과를 출력한다."""
    print("=" * 46)
    print(TITLE)
    print("=" * 46)
    print("   G H P | A F")
    print("   ------+----")
    for values in all_input_cases():
        print("   {} | {}".format(bits(values), bits(decide(*values))))
    print()
    for line in test_report().splitlines():
        print("  " + line)
    print("=" * 46)


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

    sensor_box = ttk.LabelFrame(outer, text="가상 센서 입력", padding=10)
    sensor_box.pack(fill="x")

    sensor_vars = [tk.BooleanVar(value=False) for _ in INPUT_LABELS]

    output_box = ttk.LabelFrame(outer, text="출력 장치", padding=10)
    output_box.pack(fill="x", pady=(10, 0))

    state_labels = []
    message_labels = []
    for index, label in enumerate(OUTPUT_LABELS):
        top_pad = 0 if index == 0 else 8
        ttk.Label(output_box, text=label + " :").grid(
            row=index * 2, column=0, sticky="w", pady=(top_pad, 0)
        )
        chip = tk.Label(
            output_box, text=TEXT_OFF, width=8, relief="ridge", padx=6, pady=2
        )
        chip.grid(row=index * 2, column=1, sticky="w", padx=8, pady=(top_pad, 0))
        message = ttk.Label(output_box, text=MESSAGES_OFF[index])
        message.grid(row=index * 2 + 1, column=0, columnspan=2, sticky="w")
        state_labels.append(chip)
        message_labels.append(message)

    level_box = ttk.Frame(outer)
    ttk.Label(level_box, text="현재 안전 등급 :").pack(side="left")
    level_label = tk.Label(
        level_box, text="", width=10, relief="ridge", padx=6, pady=3
    )
    level_label.pack(side="left", padx=8)

    status_label = ttk.Label(outer, text="")

    def update_output(*_args) -> None:
        """센서 상태가 바뀔 때마다 두 출력과 상태 등급을 갱신한다."""
        values = [var.get() for var in sensor_vars]
        alarm, fan = decide(*values)
        for index, result in enumerate((alarm, fan)):
            state_labels[index].config(
                text=TEXT_ON if result else TEXT_OFF,
                fg=FG_ON if result else FG_OFF,
                bg=BG_ON if result else BG_OFF,
            )
            message_labels[index].config(
                text=MESSAGES_ON[index] if result else MESSAGES_OFF[index]
            )
        text, color = safety_level(alarm, fan)
        level_label.config(text=text, fg="white", bg=color)
        status_label.config(
            text="입력 G H P = {}  ->  출력 A F = {}".format(
                bits(values), bits((alarm, fan))
            )
        )

    for row, (label, var) in enumerate(zip(INPUT_LABELS, sensor_vars)):
        ttk.Checkbutton(
            sensor_box, text=label, variable=var, command=update_output
        ).grid(row=row, column=0, sticky="w", pady=1)

    level_box.pack(fill="x", pady=(10, 0))

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
    ttk.Button(button_box, text="종료", command=root.destroy).pack(side="right")

    status_label.pack(anchor="w", pady=(10, 0))

    update_output()
    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    main()
