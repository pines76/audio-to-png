import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import math
import os
import struct

HEADER_SIZE = 8  # store original file size (8 bytes)


def file_to_png():
    input_file = filedialog.askopenfilename(title="Select audio file")
    if not input_file:
        return

    output_file = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Image", "*.png")],
        title="Save PNG image"
    )
    if not output_file:
        return

    try:
        with open(input_file, "rb") as f:
            data = f.read()

        original_size = len(data)
        header = struct.pack(">Q", original_size)
        data = header + data

        pixels_needed = math.ceil(len(data) / 3)
        width = math.ceil(math.sqrt(pixels_needed))
        height = math.ceil(pixels_needed / width)

        padded_size = width * height * 3
        data += b"\x00" * (padded_size - len(data))

        img = Image.new("RGB", (width, height))
        pixels = img.load()

        index = 0
        for y in range(height):
            for x in range(width):
                r = data[index]
                g = data[index + 1]
                b = data[index + 2]
                pixels[x, y] = (r, g, b)
                index += 3

        img.save(output_file, "PNG")

        messagebox.showinfo("Done", "Audio successfully encoded into PNG.")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def png_to_file():
    input_file = filedialog.askopenfilename(
        title="Select PNG image",
        filetypes=[("PNG Image", "*.png")]
    )
    if not input_file:
        return

    output_file = filedialog.asksaveasfilename(
        title="Save recovered audio file"
    )
    if not output_file:
        return

    try:
        img = Image.open(input_file)
        pixels = img.load()
        width, height = img.size

        data = bytearray()

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                data.append(r)
                data.append(g)
                data.append(b)

        original_size = struct.unpack(">Q", data[:HEADER_SIZE])[0]
        audio_data = data[HEADER_SIZE:HEADER_SIZE + original_size]

        with open(output_file, "wb") as f:
            f.write(audio_data)

        messagebox.showinfo("Done", "Audio successfully recovered from PNG.")

    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("Audio ↔ PNG Converter")
root.geometry("400x200")

frame = tk.Frame(root)
frame.pack(expand=True)

title = tk.Label(frame, text="Audio to PNG / PNG to Audio", font=("Arial", 14))
title.pack(pady=10)

encode_btn = tk.Button(frame, text="Audio File → PNG Image", width=25, command=file_to_png)
encode_btn.pack(pady=10)

decode_btn = tk.Button(frame, text="PNG Image → Audio File", width=25, command=png_to_file)
decode_btn.pack(pady=10)

root.mainloop()