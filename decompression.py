from tkinter import messagebox
import pickle
import os


def decompression(file):

    encode_dictionary = read_dictionary(file)
    if encode_dictionary is None:
        return None, None

    decode_dictionary = reverse_dictionary(encode_dictionary)

    binary_data = decode(file)
    return_data = decompress(binary_data, decode_dictionary)

    out_file_name = file[:file.index(" Compressed.bin")]
    out_file_name += " Decompressed.txt"
    f = open(out_file_name, "w")
    f.write(return_data)
    f.close()

    return out_file_name, encode_dictionary


def reverse_dictionary(dictionary):
    decode_dictionary = {}
    for key in dictionary:
        decode_dictionary[dictionary[key]] = key

    return decode_dictionary


def decode(file):
    try:
        input_file = open(file, "rb")
    except IOError:
        messagebox.showerror("Error", "Invalid filename")
        return

    bit_text = ""
    encoded_byte = input_file.read(1)

    while encoded_byte != b"":
        encoded_byte = ord(encoded_byte)
        bits = bin(encoded_byte)[2:].rjust(8, "0")

        bit_text += bits
        encoded_byte = input_file.read(1)

    full_data = bit_text[:8]
    extra_data = int(full_data, 2)
    full_encoded_text = bit_text[8:]
    encoded_text = full_encoded_text[:-1 * extra_data]

    return encoded_text


def decompress(binary_data, decode_dictionary):
    current_code = ""
    decoded_text = ""

    for bit in binary_data:
        current_code += bit
        if current_code in decode_dictionary:
            character = decode_dictionary[current_code]
            decoded_text += character
            current_code = ""

    return decoded_text


def read_dictionary(file):
    folder = "Dictionaries"
    root_path = os.path.dirname(os.path.abspath("main_project.py"))
    path = os.path.join(root_path, folder)

    if not os.path.exists(path):
        message = "The folder \"Dictionaries\" does not exist. It may have been moved or deleted." \
                  "\n\nPlease recompress the file to properly decompress it. "
        messagebox.showerror("Error", message)
        return

    dictionary_file_name = file[file.rindex("/") + 1:file.index(" Compressed.bin")] + " dictionary.txt"
    read_dictionary_file = os.path.join(path, dictionary_file_name)

    if not os.path.exists(read_dictionary_file):
        message = f"The file \"{dictionary_file_name}\" does not exist. It may have been moved or deleted. \n\nPlease "\
                  f"recompress the file to properly decompress it. "
        messagebox.showerror("Error", message)
        return

    read_dictionary_file = open(read_dictionary_file, "rb")
    data = read_dictionary_file.read()
    read_dictionary_file.close()

    return pickle.loads(data)
