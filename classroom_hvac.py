"""교실 자동 냉난방/환기 시스템 (입력 6개 / 출력 4개)

05_invention_starter_2out.py 를 복사해 '학생이 수정하는 부분'만 고친 파일이다.
GUI 프레임워크는 템플릿 그대로 두었다.

    입력  R: 자동 운영 모드가 켜져 있는가?
          P: 교실에 사람이 있는가?
          W: 창문이 열렸는가?
          T1: 외부 온도가 28도를 초과하는가?
          T2: 외부 온도가 18도 미만인가?
          Q: 이산화탄소 농도가 높은가?

    출력  C: 냉방,  H: 난방,  A1: 창문 닫기 경고,  A2: 창문 열기 경고

    판단 규칙
          hot  = T1 and (not T2)      더위 신호가 믿을 만한가
          cold = T2 and (not T1)      추위 신호가 믿을 만한가

          C  = R and P and (not W) and hot and (not Q)
          H  = R and P and (not W) and cold and (not Q)
          A1 = R and P and W and (hot or cold) and (not Q)
          A2 = P and (not W) and Q

    두 경고음은 창문 상태가 서로 반대다.
    닫으라는 경고는 열려 있을 때만, 열라는 경고는 닫혀 있을 때만 울린다.

    불가능한 입력 처리
          바깥 온도가 28도를 넘으면서 동시에 18도 미만일 수는 없다.
          T1 과 T2 가 함께 참이면 온도 센서가 고장 난 것으로 보고
          온도로 움직이는 출력(C, H, A1)을 모두 멈춘다.
          화면에서도 두 체크박스가 동시에 켜지지 않도록 막는다.

실행 방법:
    python classroom_hvac.py
"""

import itertools
import tkinter as tk
from tkinter import messagebox, ttk

# ============================================================
# 학생이 수정하는 부분
# ============================================================

TITLE = "교실 자동 냉난방/환기 시스템"
DESCRIPTION = "센서를 켜고 끄면 네 출력 장치의 상태가 즉시 갱신됩니다."

INPUT_LABELS = [
    "자동 운영 모드가 켜져 있다 (R)",
    "교실에 사람이 있다 (P)",
    "창문이 열렸다 (W)",
    "외부 온도가 28도를 초과한다 (T1)",
    "외부 온도가 18도 미만이다 (T2)",
    "이산화탄소 농도가 높다 (Q)",
]

# 동시에 참일 수 없는 센서 묶음. INPUT_LABELS 의 번호로 적는다.
# 3번 T1(28도 초과)과 4번 T2(18도 미만)는 물리적으로 함께 성립할 수 없으므로,
# 하나를 켜면 다른 하나가 자동으로 꺼진다.
EXCLUSIVE_INPUTS = [(3, 4)]

# 출력 장치 네 개의 이름과 상태 문구 (순서를 맞춘다)
OUTPUT_LABELS = ["냉방 (C)", "난방 (H)", "창문 닫기 경고 (A1)", "창문 열기 경고 (A2)"]
MESSAGES_ON = [
    "실내가 더워 냉방을 가동합니다.",
    "실내가 추워 난방을 가동합니다.",
    "냉난방 효율을 위해 창문을 닫아 주세요.",
    "이산화탄소 농도가 높습니다. 창문을 여세요.",
]
MESSAGES_OFF = [
    "냉방은 멈춰 있습니다.",
    "난방은 멈춰 있습니다.",
    "창문 닫기 경고음은 울리지 않습니다.",
    "공기 상태는 정상입니다.",
]


def decide(auto_mode, person, window_open, too_hot, too_cold, co2_high):
    """판단 규칙: 네 출력의 목적이 다르므로 조건식도 다르다."""
    # 28도 초과이면서 동시에 18도 미만일 수는 없다.
    # 두 신호가 함께 들어오면 센서 고장으로 보고 온도 판단을 하지 않는다.
    hot = too_hot and not too_cold
    cold = too_cold and not too_hot

    # 냉난방은 창문이 닫혀 있어야 의미가 있고, 환기가 먼저인 상황에서는 멈춘다.
    cooling = auto_mode and person and not window_open and hot and not co2_high
    heating = auto_mode and person and not window_open and cold and not co2_high

    # 창문이 열려 있을 때만 닫으라고 알린다. 이미 닫혀 있으면 알릴 이유가 없다.
    close_warning = auto_mode and person and window_open and (hot or cold) and not co2_high

    # 공기 질은 안전 문제이므로 자동 운영 모드와 상관없이 경고한다.
    # 다만 창문이 이미 열려 있으면 열라고 할 이유가 없다.
    open_warning = person and not window_open and co2_high

    return cooling, heating, close_warning, open_warning


# 제품 시험표: ((R, P, W, T1, T2, Q), (C, H, A1, A2))
# 진리표 64줄을 그대로 옮겨 적었다. 0 은 False, 1 은 True 를 뜻한다.
TEST_CASES = [
    ((0, 0, 0, 0, 0, 0), (0, 0, 0, 0)),
    ((0, 0, 0, 0, 0, 1), (0, 0, 0, 0)),
    ((0, 0, 0, 0, 1, 0), (0, 0, 0, 0)),
    ((0, 0, 0, 0, 1, 1), (0, 0, 0, 0)),
    ((0, 0, 0, 1, 0, 0), (0, 0, 0, 0)),
    ((0, 0, 0, 1, 0, 1), (0, 0, 0, 0)),
    ((0, 0, 0, 1, 1, 0), (0, 0, 0, 0)),
    ((0, 0, 0, 1, 1, 1), (0, 0, 0, 0)),
    ((0, 0, 1, 0, 0, 0), (0, 0, 0, 0)),
    ((0, 0, 1, 0, 0, 1), (0, 0, 0, 0)),
    ((0, 0, 1, 0, 1, 0), (0, 0, 0, 0)),
    ((0, 0, 1, 0, 1, 1), (0, 0, 0, 0)),
    ((0, 0, 1, 1, 0, 0), (0, 0, 0, 0)),
    ((0, 0, 1, 1, 0, 1), (0, 0, 0, 0)),
    ((0, 0, 1, 1, 1, 0), (0, 0, 0, 0)),
    ((0, 0, 1, 1, 1, 1), (0, 0, 0, 0)),
    ((0, 1, 0, 0, 0, 0), (0, 0, 0, 0)),
    ((0, 1, 0, 0, 0, 1), (0, 0, 0, 1)),
    ((0, 1, 0, 0, 1, 0), (0, 0, 0, 0)),
    ((0, 1, 0, 0, 1, 1), (0, 0, 0, 1)),
    ((0, 1, 0, 1, 0, 0), (0, 0, 0, 0)),
    ((0, 1, 0, 1, 0, 1), (0, 0, 0, 1)),
    ((0, 1, 0, 1, 1, 0), (0, 0, 0, 0)),
    ((0, 1, 0, 1, 1, 1), (0, 0, 0, 1)),
    ((0, 1, 1, 0, 0, 0), (0, 0, 0, 0)),
    ((0, 1, 1, 0, 0, 1), (0, 0, 0, 0)),
    ((0, 1, 1, 0, 1, 0), (0, 0, 0, 0)),
    ((0, 1, 1, 0, 1, 1), (0, 0, 0, 0)),
    ((0, 1, 1, 1, 0, 0), (0, 0, 0, 0)),
    ((0, 1, 1, 1, 0, 1), (0, 0, 0, 0)),
    ((0, 1, 1, 1, 1, 0), (0, 0, 0, 0)),
    ((0, 1, 1, 1, 1, 1), (0, 0, 0, 0)),
    ((1, 0, 0, 0, 0, 0), (0, 0, 0, 0)),
    ((1, 0, 0, 0, 0, 1), (0, 0, 0, 0)),
    ((1, 0, 0, 0, 1, 0), (0, 0, 0, 0)),
    ((1, 0, 0, 0, 1, 1), (0, 0, 0, 0)),
    ((1, 0, 0, 1, 0, 0), (0, 0, 0, 0)),
    ((1, 0, 0, 1, 0, 1), (0, 0, 0, 0)),
    ((1, 0, 0, 1, 1, 0), (0, 0, 0, 0)),
    ((1, 0, 0, 1, 1, 1), (0, 0, 0, 0)),
    ((1, 0, 1, 0, 0, 0), (0, 0, 0, 0)),
    ((1, 0, 1, 0, 0, 1), (0, 0, 0, 0)),
    ((1, 0, 1, 0, 1, 0), (0, 0, 0, 0)),
    ((1, 0, 1, 0, 1, 1), (0, 0, 0, 0)),
    ((1, 0, 1, 1, 0, 0), (0, 0, 0, 0)),
    ((1, 0, 1, 1, 0, 1), (0, 0, 0, 0)),
    ((1, 0, 1, 1, 1, 0), (0, 0, 0, 0)),
    ((1, 0, 1, 1, 1, 1), (0, 0, 0, 0)),
    ((1, 1, 0, 0, 0, 0), (0, 0, 0, 0)),
    ((1, 1, 0, 0, 0, 1), (0, 0, 0, 1)),
    ((1, 1, 0, 0, 1, 0), (0, 1, 0, 0)),
    ((1, 1, 0, 0, 1, 1), (0, 0, 0, 1)),
    ((1, 1, 0, 1, 0, 0), (1, 0, 0, 0)),
    ((1, 1, 0, 1, 0, 1), (0, 0, 0, 1)),
    ((1, 1, 0, 1, 1, 0), (0, 0, 0, 0)),
    ((1, 1, 0, 1, 1, 1), (0, 0, 0, 1)),
    ((1, 1, 1, 0, 0, 0), (0, 0, 0, 0)),
    ((1, 1, 1, 0, 0, 1), (0, 0, 0, 0)),
    ((1, 1, 1, 0, 1, 0), (0, 0, 1, 0)),
    ((1, 1, 1, 0, 1, 1), (0, 0, 0, 0)),
    ((1, 1, 1, 1, 0, 0), (0, 0, 1, 0)),
    ((1, 1, 1, 1, 0, 1), (0, 0, 0, 0)),
    ((1, 1, 1, 1, 1, 0), (0, 0, 0, 0)),
    ((1, 1, 1, 1, 1, 1), (0, 0, 0, 0)),
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
    """decide()의 결과를 항상 길이 4의 튜플로 정리한다."""
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
        return "TEST_CASES가 비어 있습니다.\n네 출력의 예상값을 먼저 채우세요."
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
        lines.append("네 출력의 조건식을 각각 다시 확인해 보세요.")
    else:
        lines.append("")
        lines.append("모든 입력 조합에서 네 출력이 의도한 대로 작동합니다.")
    return "\n".join(lines)


def open_truth_table(parent) -> None:
    """전체 입력 조합에 대한 네 출력의 예상값과 실제값을 보여 주는 창."""
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
        """센서 상태가 바뀔 때마다 네 출력을 함께 갱신한다."""
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

    def make_toggle(index):
        """센서를 켤 때, 함께 참일 수 없는 센서는 자동으로 끈다."""

        def on_toggle() -> None:
            if sensor_vars[index].get():
                for group in EXCLUSIVE_INPUTS:
                    if index in group:
                        for other in group:
                            if other != index:
                                sensor_vars[other].set(False)
            update_output()

        return on_toggle

    for row, (label, var) in enumerate(zip(INPUT_LABELS, sensor_vars)):
        ttk.Checkbutton(
            sensor_box, text=label, variable=var, command=make_toggle(row)
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
