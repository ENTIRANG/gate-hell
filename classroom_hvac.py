"""교실 자동 냉난방/환기 시스템 (입력 6개 / 출력 4개)

프로젝트.md 의 명세를 그대로 옮긴 프로토타입이다.

    입력  R: 자동 운영 모드가 켜져 있는가?
          P: 교실에 사람이 있는가?
          W: 창문이 열렸는가?
          T1: 외부 온도가 28도를 초과하는가?
          T2: 외부 온도가 18도 미만인가?
          Q: 이산화탄소 농도가 높은가?

    출력  C: 냉방
          H: 난방
          A1: 창문 닫기 경고음
          A2: 창문 열기 경고음

    판단 규칙
          C  = R and P and (not W) and T1 and (not Q)
          H  = R and P and (not W) and T2 and (not Q)
          A1 = R and P and (T1 or T2) and (not Q)
          A2 = P and Q

논리 연산은 and, or, not 만 사용한다. 비트 연산자(&, |, ^, ~)는 쓰지 않는다.

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
DESCRIPTION = "센서 6개를 조합하면 출력 장치 4개의 상태가 즉시 갱신됩니다."

INPUT_LABELS = [
    "자동 운영 모드가 켜져 있다 (R)",
    "교실에 사람이 있다 (P)",
    "창문이 열렸다 (W)",
    "외부 온도가 28도를 초과한다 (T1)",
    "외부 온도가 18도 미만이다 (T2)",
    "이산화탄소 농도가 높다 (Q)",
]

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
    """센서 6개를 읽어 출력 4개를 결정한다.

    출력마다 목적이 다르므로 조건식도 서로 다르다.
    특히 A2 는 자동 운영 모드(R)와 무관하다. 사람이 있는데 공기가 나쁘면
    자동 운영을 꺼 두었더라도 알려야 하기 때문이다.
    """
    # 냉난방은 창문이 닫혀 있어야 의미가 있고, 환기가 먼저인 상황에서는 멈춘다.
    cooling = auto_mode and person and not window_open and too_hot and not co2_high
    heating = auto_mode and person and not window_open and too_cold and not co2_high

    # 바깥 온도가 극단적이면 창문을 닫으라고 알린다.
    close_window_warning = auto_mode and person and (too_hot or too_cold) and not co2_high

    # 공기 질은 안전 문제이므로 자동 운영 모드와 상관없이 경고한다.
    open_window_warning = person and co2_high

    return cooling, heating, close_window_warning, open_window_warning


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
    ((0, 1, 1, 0, 0, 1), (0, 0, 0, 1)),
    ((0, 1, 1, 0, 1, 0), (0, 0, 0, 0)),
    ((0, 1, 1, 0, 1, 1), (0, 0, 0, 1)),
    ((0, 1, 1, 1, 0, 0), (0, 0, 0, 0)),
    ((0, 1, 1, 1, 0, 1), (0, 0, 0, 1)),
    ((0, 1, 1, 1, 1, 0), (0, 0, 0, 0)),
    ((0, 1, 1, 1, 1, 1), (0, 0, 0, 1)),
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
    ((1, 1, 0, 0, 1, 0), (0, 1, 1, 0)),
    ((1, 1, 0, 0, 1, 1), (0, 0, 0, 1)),
    ((1, 1, 0, 1, 0, 0), (1, 0, 1, 0)),
    ((1, 1, 0, 1, 0, 1), (0, 0, 0, 1)),
    ((1, 1, 0, 1, 1, 0), (1, 1, 1, 0)),
    ((1, 1, 0, 1, 1, 1), (0, 0, 0, 1)),
    ((1, 1, 1, 0, 0, 0), (0, 0, 0, 0)),
    ((1, 1, 1, 0, 0, 1), (0, 0, 0, 1)),
    ((1, 1, 1, 0, 1, 0), (0, 0, 1, 0)),
    ((1, 1, 1, 0, 1, 1), (0, 0, 0, 1)),
    ((1, 1, 1, 1, 0, 0), (0, 0, 1, 0)),
    ((1, 1, 1, 1, 0, 1), (0, 0, 0, 1)),
    ((1, 1, 1, 1, 1, 0), (0, 0, 1, 0)),
    ((1, 1, 1, 1, 1, 1), (0, 0, 0, 1)),
]

# ============================================================
# GUI 프레임워크: 처음에는 수정하지 않음
# ============================================================

INPUT_CODES = ["R", "P", "W", "T1", "T2", "Q"]
OUTPUT_CODES = ["C", "H", "A1", "A2"]

INPUT_COUNT = len(INPUT_LABELS)
OUTPUT_COUNT = len(OUTPUT_LABELS)

TEXT_ON = "작동"
TEXT_OFF = "정지"
FG_ON, BG_ON = "#b71c1c", "#ffe0e0"
FG_OFF, BG_OFF = "#1b5e20", "#e3f1e3"


def bits(values) -> str:
    """(True, False) 를 '1 0' 처럼 0과 1로 나타낸다."""
    return " ".join(str(int(value)) for value in values)


def binary_text(values) -> str:
    """(True, True, False) 를 '110' 처럼 붙여 쓴 2진수로 나타낸다."""
    return "".join(str(int(bool(value))) for value in values)


def to_decimal(values) -> int:
    """2진수로 늘어놓은 참·거짓을 10진수 하나로 바꾼다.

    왼쪽이 가장 큰 자리다. 자리를 옮길 때마다 2를 곱하고 다음 자리를 더한다.
    비트 연산자(<<, |)를 쓰지 않고 곱셈과 덧셈만으로 계산한다.
    """
    number = 0
    for value in values:
        number = number * 2 + int(bool(value))
    return number


def all_input_cases():
    """입력 개수에 맞는 64가지 조합을 순서대로 만들어 준다."""
    return list(itertools.product((False, True), repeat=INPUT_COUNT))


def outputs_of(values):
    """decide()의 결과를 항상 길이 4의 불리언 튜플로 정리한다."""
    result = decide(*values)
    if not isinstance(result, tuple) or len(result) != OUTPUT_COUNT:
        raise ValueError(
            "decide 함수는 출력 {}개를 튜플로 돌려주어야 합니다.".format(OUTPUT_COUNT)
        )
    return tuple(bool(item) for item in result)


def impossible_input(values) -> bool:
    """물리적으로 불가능한 센서 조합인지 알려 준다.

    바깥 온도가 28도를 넘으면서 동시에 18도 미만일 수는 없다.
    명세에는 이 조합을 막는 규칙이 없으므로, 판단을 바꾸지 않고 화면에만 표시한다.
    """
    too_hot = values[3]
    too_cold = values[4]
    return bool(too_hot) and bool(too_cold)


def check_test_cases() -> str:
    """TEST_CASES의 형식을 검사한다. 문제가 없으면 빈 문자열을 돌려준다."""
    if not TEST_CASES:
        return "TEST_CASES가 비어 있습니다.\n진리표의 값을 먼저 채우세요."
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
            return "{}번째 예상 출력이 {}개가 아닙니다.".format(number, OUTPUT_COUNT)
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
    lines.append("출력 순서: {}".format(", ".join(OUTPUT_CODES)))
    if failures:
        lines.append("")
        lines.append("실패한 입력 조합")
        lines.extend(failures[:12])
        if len(failures) > 12:
            lines.append("... 외 {}건".format(len(failures) - 12))
        lines.append("")
        lines.append("네 출력의 조건식을 각각 다시 확인해 보세요.")
    else:
        lines.append("")
        lines.append("64가지 입력 조합 모두 설계한 대로 작동합니다.")
    return "\n".join(lines)


def print_truth_table_and_tests() -> None:
    """터미널에 진리표와 자동 테스트 결과를 출력한다."""
    print("=" * 52)
    print(TITLE)
    print("=" * 52)
    print("   R P W T1 T2 Q | C H A1 A2")
    print("   ---------------+-----------")
    for values in all_input_cases():
        mark = "   <- 불가능한 조합" if impossible_input(values) else ""
        print("   {} | {}{}".format(bits(values), bits(outputs_of(values)), mark))
    print()
    for line in test_report().splitlines():
        print("  " + line)
    print("=" * 52)


def open_truth_table(parent) -> None:
    """64가지 입력 조합의 예상값과 실제값을 표로 보여 주는 창."""
    expected_of = dict(TEST_CASES) if not check_test_cases() else {}

    window = tk.Toplevel(parent)
    window.title("전체 입력 진리표 (64가지)")

    frame = ttk.Frame(window, padding=12)
    frame.pack(fill="both", expand=True)

    only_active = tk.BooleanVar(value=False)

    columns = ["dec", "bin"] + INPUT_CODES + OUTPUT_CODES + ["check"]
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)

    # 입력 6칸을 2진수로 읽으면 0부터 63까지의 10진수가 된다. 진리표의 줄 번호와 같다.
    tree.heading("dec", text="10진수")
    tree.column("dec", width=54, anchor="center")
    tree.heading("bin", text="2진수")
    tree.column("bin", width=70, anchor="center")
    for code in INPUT_CODES:
        tree.heading(code, text=code)
        tree.column(code, width=34, anchor="center")
    for code in OUTPUT_CODES:
        tree.heading(code, text=code)
        tree.column(code, width=40, anchor="center")
    tree.heading("check", text="검증")
    tree.column("check", width=52, anchor="center")

    tree.tag_configure("on", background="#ffe9e9")
    tree.tag_configure("impossible", background="#eeeeee", foreground="#999999")
    tree.tag_configure("bad", background="#ffcdd2")

    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)

    def fill() -> None:
        tree.delete(*tree.get_children())
        for values in all_input_cases():
            actual = outputs_of(values)
            if only_active.get() and not any(actual):
                continue

            expected = expected_of.get(values)
            if expected is None:
                mark = "?"
            elif tuple(bool(item) for item in expected) == actual:
                mark = "O"
            else:
                mark = "X"

            if mark == "X":
                tag = "bad"
            elif impossible_input(values):
                tag = "impossible"
            elif any(actual):
                tag = "on"
            else:
                tag = ""

            row = [to_decimal(values), binary_text(values)]
            row += [int(value) for value in values]
            row += [int(value) for value in actual]
            row += [mark]
            tree.insert("", "end", values=row, tags=(tag,))

    ttk.Checkbutton(
        frame,
        text="출력이 하나라도 켜지는 행만 보기",
        variable=only_active,
        command=fill,
    ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

    tree.grid(row=1, column=0, sticky="nsew")
    scroll.grid(row=1, column=1, sticky="ns")
    frame.rowconfigure(1, weight=1)
    frame.columnconfigure(0, weight=1)

    note = "회색 행: 28도 초과와 18도 미만이 동시에 참인 불가능한 조합"
    ttk.Label(frame, text=note).grid(
        row=2, column=0, columnspan=2, sticky="w", pady=(8, 0)
    )
    ttk.Button(frame, text="닫기", command=window.destroy).grid(
        row=3, column=0, columnspan=2, pady=(8, 0)
    )

    fill()


def main() -> None:
    print_truth_table_and_tests()

    root = tk.Tk()
    root.title(TITLE)

    outer = ttk.Frame(root, padding=16)
    outer.pack(fill="both", expand=True)

    ttk.Label(outer, text=TITLE, font=("TkDefaultFont", 14, "bold")).pack(anchor="w")
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

    # 이 수업의 목표는 상태를 0과 1로 적어 내려가는 것이다.
    # 센서와 출력 장치의 현재 상태를 2진수로, 그리고 10진수로 함께 보여 준다.
    binary_box = ttk.LabelFrame(outer, text="이진법 표현", padding=10)
    binary_box.pack(fill="x", pady=(10, 0))

    mono = ("TkFixedFont", 11)
    mono_bold = ("TkFixedFont", 13, "bold")

    def spaced(items) -> str:
        """각 칸을 세 글자 폭으로 맞춰 위아래 줄을 정렬한다."""
        return "".join("{:<3}".format(item) for item in items)

    ttk.Label(binary_box, text="입력", font=mono).grid(row=0, column=0, sticky="w")
    ttk.Label(binary_box, text=spaced(INPUT_CODES), font=mono).grid(
        row=0, column=1, sticky="w", padx=(10, 0)
    )
    input_bits_label = ttk.Label(binary_box, text="", font=mono_bold)
    input_bits_label.grid(row=1, column=1, sticky="w", padx=(10, 0))
    input_number_label = ttk.Label(binary_box, text="", font=mono)
    input_number_label.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=(2, 8))

    ttk.Label(binary_box, text="출력", font=mono).grid(row=3, column=0, sticky="w")
    ttk.Label(binary_box, text=spaced(OUTPUT_CODES), font=mono).grid(
        row=3, column=1, sticky="w", padx=(10, 0)
    )
    output_bits_label = ttk.Label(binary_box, text="", font=mono_bold)
    output_bits_label.grid(row=4, column=1, sticky="w", padx=(10, 0))
    output_number_label = ttk.Label(binary_box, text="", font=mono)
    output_number_label.grid(row=5, column=1, sticky="w", padx=(10, 0), pady=(2, 0))

    warning_label = ttk.Label(outer, text="", foreground="#ef6c00")
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

        input_bits_label.config(text=spaced(int(value) for value in values))
        input_number_label.config(
            text="2진수 {}  =  10진수 {}   (진리표 {}번 줄)".format(
                binary_text(values), to_decimal(values), to_decimal(values)
            )
        )
        output_bits_label.config(text=spaced(int(value) for value in results))
        output_number_label.config(
            text="2진수 {}  =  10진수 {}".format(
                binary_text(results), to_decimal(results)
            )
        )

        if impossible_input(values):
            warning_label.config(
                text="주의: 28도 초과(T1)와 18도 미만(T2)은 동시에 참일 수 없습니다."
            )
        else:
            warning_label.config(text="")

        status_label.config(text="")

    for row, (label, var) in enumerate(zip(INPUT_LABELS, sensor_vars)):
        ttk.Checkbutton(
            sensor_box, text=label, variable=var, command=update_output
        ).grid(row=row, column=0, sticky="w", pady=1)

    warning_label.pack(anchor="w", pady=(10, 0))

    button_box = ttk.Frame(outer)
    button_box.pack(fill="x", pady=(12, 0))

    def reset_sensors() -> None:
        for var in sensor_vars:
            var.set(False)
        update_output()

    ttk.Button(button_box, text="초기화", command=reset_sensors).pack(side="left")
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
