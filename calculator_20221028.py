from tkinter import *
import tkinter.font

record = [] # 계산 기록 저장

window = Tk()
window.title("My Calculator")
window.resizable(False, False)

font_base = tkinter.font.Font(size=9, weight="bold")

displayInput = Entry(window, width=39, bg="white", justify="right")
displayInput.grid(row=0, column=0, columnspan=5, ipady=5)

displayOutput = Label(window, width=37, bg="#FAF2C2", padx=3, pady=3, wraplength=250)
displayOutput.grid(row=1, column=0, columnspan=5, padx=3, pady=3)

displayBIN = Label(window, wraplength=210)
displayOCT = Label(window, wraplength=210)
displayHEX = Label(window, wraplength=210)
displayBIN.grid(row=2, column=1, columnspan=4, sticky="w")
displayOCT.grid(row=3, column=1, columnspan=4, sticky="w")
displayHEX.grid(row=4, column=1, columnspan=4, sticky="w")

button_list = [
    '7', '8', '9', '/', 'AC',
    '4', '5', '6', '*', 'C',
    '1', '2', '3', '-', '^2',
    '0', '.', '=', '+', '계산기록'
]

previous = "AC"
operator_list = ['/', '*', '-', '+', '.', '^2']

global result
result = None

def resultInput():
    global result

    s = str(result)
    displayInput.insert(END, "=")
    displayOutput.config(text=s)

    displayBIN.config(text=convert_base(result, 2))
    displayOCT.config(text=convert_base(result, 8))
    displayHEX.config(text=convert_base(result, 16))

    record.append(displayInput.get())
    record.append(s)


def clear():
    displayInput.delete(0, END)
    displayOutput.config(text="")
    displayBIN.config(text="")
    displayOCT.config(text="")
    displayHEX.config(text="")
    previous = "AC"


# 원하는 진수(16진수까지)로 변환해주는 함수
def convert_base(num, base):
    result_list = []
    hex_list = ['A', 'B', 'C', 'D', 'E', 'F']

    # base는 2에서 16 사이의 숫자
    if base < 2 or base > 16:
        return None

    num = int(num)

    # 0인 경우 0 반환
    if num == 0:
        return str(0)

    # base 변환
    while num > 0:
        remainder = num % base
        if remainder > 9:
            # 10 이상의 숫자는 hex_list의 문자를 사용
            result_list.append(hex_list[remainder - 10])
        else:
            result_list.append(str(remainder))
        num //= base
    result_list.reverse()

    return ''.join(result_list)


def click(key):
    global previous
    global result

    if previous == "=" and key != "계산기록":
        if key == "=":
            return None

        # '='을 누른 다음 새로운 키를 눌렀을 때 입력창 비우기
        displayInput.delete(0, END)

        # 연산자를 누른 경우 연산이 이어지게 하기
        if key in operator_list:
            s = displayOutput.cget("text")
            displayInput.insert(END, s)

    # 연산자 키를 누른 경우
    elif key in operator_list + ["="]:

        # 연산자를 연속으로 누른 경우
        if previous in operator_list:
            s = displayInput.get()[:-1]
            displayInput.delete(len(s))

        # 입력창이 빈 상태에서 연산자를 누른 경우
        elif previous == "AC":
            displayInput.insert(END, "0")

    # 제곱 후 이어서 연산하기
    if previous == "^2":
        displayInput.delete(0, END)
        displayInput.insert(END, result)

    if key == "=":
        result = eval(displayInput.get())
        resultInput()

    elif key == "AC":
        clear()

    elif key == "C":
        clear()
        if len(record) > 3:
            result = record[-3]

            displayInput.insert(END, record[-4])
            displayOutput.config(text=result)

            displayBIN.config(text=convert_base(result, 2))
            displayOCT.config(text=convert_base(result, 8))
            displayHEX.config(text=convert_base(result, 16))

        previous = "="

        return None

    elif key == "계산기록":
        new_window = Tk()

        for i in range(0, len(record), 2):
            Label(new_window, text=record[i] + record[i + 1], width=50, wraplength=300)\
                .pack(padx=5, pady=3)

        return None

    # 제곱
    elif key == "^2":
        # 연산식이 있을때 제곱
        if previous != "=":
            result = eval(displayInput.get())

        clear()
        displayInput.insert(END, result)
        result = result ** 2
        displayInput.insert(END, "^2 ")

        resultInput()

    else:
        displayInput.insert(END, key)

    previous = key


row_index = 2
col_index = 0
for base in ["BIN", "OCT", "HEX"]:
    Label(window, text=base, font=font_base).grid(row=row_index, column=0)
    row_index += 1

for button_text in button_list:
    def process(t=button_text):
        click(t)


    if col_index > 2:
        bg_color = "#676E9E"
        fg_color = "white"
    elif button_text == "=":
        bg_color = "#D7DBF6"
        fg_color = "black"
    else:
        bg_color = "#FFFFFF"
        fg_color = "black"

    Button(window, text=button_text, width=5, padx=4, pady=4, fg=fg_color, bg=bg_color,
           relief="flat", command=process).grid(row=row_index, column=col_index, pady=2)
    col_index += 1
    if col_index > 4:
        row_index += 1
        col_index = 0

window = mainloop()
