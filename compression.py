from tkinter import messagebox
from huffman_tree import *
import pickle
import os


def compression(file):

    try:
        file_name = open(file, "r")
    except IOError:
        messagebox.showerror("Error", "Invalid filename try select file again")
        return None, None

    text = file_name.read()
    file_name.close()

    if len(text) == 0:
        messagebox.showwarning("Warning", "Empty text file")
        return None, None

    nodes = node(text)
    root = tree(nodes)

    code = ""
    huffman_code = {}
    encode(root, code, huffman_code)

    binary = binary_code(text, huffman_code)
    string = compress(binary)
    if string is None:
        return None, None

    outfile = file[:len(file) - 4] + " Compressed.bin"
    f = open(outfile, "wb")
    f.write(string)
    f.close()

    write_dictionary(file, huffman_code)

    return outfile, huffman_code


def binary_code(text, huffman):
    if "0" in text or "1" in text:
        j = 0
        index = [i for i, ltr in enumerate(text) if ltr == "0" or ltr == "1"]
        while j < len(index):
            text = text[:index[j]] + huffman[text[index[j]]] + text[index[j] + 1:]
            j += 1
            if j < len(index):
                index[j] += len(huffman[text[index[j]]]) - 1
    for ch in huffman:
        if ch == "0" or ch == "1":
            continue
        text = text.replace(ch, huffman[ch])

    extra_code = (8 - len(text)) % 8
    for i in range(extra_code):
        text += "0"

    extra = "{0:08b}".format(extra_code)

    return extra + text


def compress(binary):
    if len(binary) % 8 != 0:
        messagebox.showerror("Error", "Encoded text not padded properly try compress file again")
        return

    string = bytearray()
    for i in range(0, len(binary), 8):
        string.append(int(binary[i:i + 8], 2))

    return bytes(string)


def write_dictionary(file, huffman):
    folder = "Dictionaries"
    root_path = os.path.dirname(os.path.abspath("main_project.py"))
    path = os.path.join(root_path, folder)

    if not os.path.exists(path):
        os.makedirs(path)

    dictionary_file_name = file[file.rindex("/") + 1:len(file) - 4] + " dictionary.txt"
    write_dictionary_file = os.path.join(path, dictionary_file_name)

    dictionary_file = open(write_dictionary_file, "wb")
    pickle.dump(huffman, dictionary_file)
    dictionary_file.close()
