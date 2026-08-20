"""00. 실습 환경 확인

이 프로그램은 두 가지를 확인한다.
  1) 지금 사용하고 있는 Python 버전
  2) tkinter가 정상적으로 동작하는지

터미널(명령 프롬프트)에서 다음과 같이 실행한다.
    python 00_environment_check.py
python 명령이 인식되지 않으면 py 명령을 사용한다.
    py 00_environment_check.py

작은 창이 열리고 "Python과 tkinter가 정상적으로 작동합니다."라는
문구가 보이면 실습 준비가 끝난 것이다.
"""

import sys
import tkinter as tk
from tkinter import ttk


def print_environment_info() -> None:
    """터미널에 실습 환경 정보를 출력한다."""
    line = "=" * 44
    print(line)
    print("실습 환경 확인")
    print(line)
    print("Python 버전 :", sys.version.split()[0])
    print("tkinter 버전:", tk.TkVersion)
    print("외부 패키지는 설치하지 않아도 된다.")
    print(line)


def main() -> None:
    print_environment_info()

    root = tk.Tk()
    root.title("실습 환경 확인")

    frame = ttk.Frame(root, padding=24)
    frame.pack(fill="both", expand=True)

    ttk.Label(
        frame,
        text="Python과 tkinter가 정상적으로 작동합니다.",
        font=("TkDefaultFont", 13, "bold"),
    ).pack(pady=(0, 12))

    ttk.Label(
        frame,
        text="Python {}  /  tkinter {}".format(
            sys.version.split()[0], tk.TkVersion
        ),
    ).pack(pady=(0, 4))

    ttk.Label(
        frame,
        text="이 창을 닫고 다음 실습 파일을 열면 된다.",
    ).pack(pady=(0, 16))

    ttk.Button(frame, text="닫기", command=root.destroy).pack()

    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    main()
