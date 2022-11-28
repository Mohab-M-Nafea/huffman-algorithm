from compression import *
from decompression import *
import threading
import time
import os
from functools import partial
from tkinter import *
from tkinter import ttk
from tkinter import filedialog


def header_window(huffman_code):
    result = Tk()
    result.title("Header info")
    result.configure(bg="white")

    width = result.winfo_screenwidth()
    height = result.winfo_screenheight()
    result.geometry("{}x{}+{}+{}".format(width, height, -10, 0))

    header_label = Label(result,
                         text="Header info",
                         width=90,
                         height=3,
                         fg="red",
                         bg="white",
                         font=("Courier", 20))
    header_label.pack()

    canvas = Canvas(result,
                    background="white",
                    width=910,
                    height=580)
    canvas.place(x=width / 8, y=100)

    scrollbar = ttk.Scrollbar(result,
                              orient=VERTICAL,
                              command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    frame = Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.bind('<Configure>', lambda x: canvas.config(scrollregion=canvas.bbox("all")))

    def table(column, data):
        table_label = Label(frame,
                            text=data,
                            width=20,
                            font=("Courier", 14),
                            bg="white",
                            borderwidth=3,
                            relief="ridge")
        table_label.grid(row=row, column=column)

    row = 0
    head_arr = ["Character", "Byte", "Code", "New Code"]
    for index in range(len(head_arr)):
        table(index, head_arr[index])

    row += 1
    for ch in huffman_code:
        byte = ord(ch)
        table(1, byte)
        binary = bin(byte)
        code = binary[2:].rjust(8, "0")
        table(2, code)
        new_code = huffman_code[ch]
        table(3, new_code)
        if ch == "\n":
            ch = "New Line"
        elif ch == "\t":
            ch = "Tap"
        elif ch == " ":
            ch = "Space"
        table(0, ch)
        row += 1

    result.mainloop()


def info(filename, file_out, state_process, state, execution_time):
    global info_flag
    if info_flag:
        window.geometry("800x300")
        label.place_forget()
        info_message.place_forget()
        info_flag = False
        return

    original = os.path.getsize(filename)
    new = os.path.getsize(file_out)

    original_size = f"Original file size: {original / 1024.0} KB"
    new_size = f"{state_process} file size: {new / 1024.0} KB"

    rate = ((new - original) / new) * 100 if state_process == "Decompressed" else ((original - new) / original) * 100
    state_rate = "{} file to about {:.04f}% of original".format(state_process, rate)

    process_time = "Execution time for {}: {:.06f} seconds".format(state, execution_time)
    message = original_size + "\n\n" + new_size + "\n\n" + state_rate + "\n\n" + process_time + "\n\n"

    window.geometry("800x420")

    label.place(x=300, y=140)

    info_message["text"] = message
    info_message.place(x=20, y=220)

    info_flag = True


def start(filename, state):
    start_time = time.time()
    start_button.place_forget()
    button_explore["state"] = DISABLED

    progress.place(x=350, y=80)

    if " Compressed.bin" in filename:
        state_process = "Decompressed"
        file_out, code = decompression(filename)
    else:
        state_process = "Compressed"
        file_out, code = compression(filename)

    button_explore["state"] = NORMAL

    progress.place_forget()

    if file_out is None:
        return

    info_button["command"] = partial(info,
                                     filename,
                                     file_out,
                                     state_process,
                                     state,
                                     time.time() - start_time)
    info_button.place(x=280, y=80)

    header_button["command"] = partial(header_window, code)
    header_button.place(x=400, y=80)


def browse_file():

    filename = filedialog.askopenfilename(title="Select a File",
                                          filetypes=[("Text files",
                                                      "*.txt* *.bin*")])
    if filename == "":
        return

    window.geometry("800x300")
    header_button.place_forget()
    info_button.place_forget()
    label.place_forget()
    info_message.place_forget()

    file = filename[filename.rindex("/") + 1:]
    if " Compressed.bin" in filename:
        state = "Decompression"
        label_file_explorer.configure(text=f"You selected: {file} file to decompress it")
    else:
        state = "Compression"
        label_file_explorer.configure(text=f"You selected: {file} file to compress it")

    thread = threading.Thread(target=start, args=(filename, state))

    start_button["text"] = f"Start {state}"
    start_button.place(x=360, y=80)
    start_button["command"] = thread.start

    while thread.is_alive():
        if close_flag:
            break

    thread.daemon = True


def close():
    global close_flag
    close_flag = True
    window.destroy()


if __name__ == '__main__':
    close_flag = False
    info_flag = False

    window = Tk()
    window.title("2M Compressor")
    window.geometry("800x300")
    window.config(background="white")
    window.protocol("WM_DELETE_WINDOW", close)

    icon = PhotoImage(file="2M Compressor.png")
    window.iconphoto(True, icon)

    label_file_explorer = Label(window,
                                text="Click Browse Files to select a file to compress or decompress",
                                fg="blue",
                                bg="white",
                                font=("Courier", 12))

    button_explore = ttk.Button(window,
                                text="Browse Files",
                                command=browse_file)

    start_button = ttk.Button(window)

    info_button = ttk.Button(window,
                             text="show info")

    header_button = ttk.Button(window,
                               text="show header window")

    progress = Label(window,
                     text="In progress",
                     fg="blue",
                     bg="white",
                     font=("Courier", 12))

    label = Label(window,
                  text="Running info",
                  fg="red",
                  bg="white",
                  font=("Courier", 20))

    info_message = Message(window,
                           width=750,
                           bg="white",
                           font=("Courier", 14))

    label_file_explorer.place(x=20, y=20)

    button_explore.place(x=700, y=20)

    window.mainloop()
