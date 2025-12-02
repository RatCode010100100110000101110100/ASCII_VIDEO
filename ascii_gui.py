import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

def select_input():
    path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
    if path:
        input_var.set(path)

def run_conversion():
    input_path = input_var.get()
    output_path = output_var.get()
    if not input_path or not output_path:
        messagebox.showerror("Error", "Please set input and output files.")
        return

    mode = mode_var.get()
    background = bg_var.get()
    num_cols = cols_var.get()
    scale = scale_var.get()
    fps = fps_var.get()
    overlay = overlay_var.get()

    cmd = [
        "python3", "ascii_video.py",
        "--input", input_path,
        "--output", output_path,
        "--mode", mode,
        "--background", background,
        "--num_cols", str(num_cols),
        "--scale", str(scale),
        "--fps", str(fps),
        "--overlay_ratio", str(overlay)
    ]

    # Run the conversion process (blocking)
    subprocess.run(cmd)
    messagebox.showinfo("Done", "Video ASCII conversion completed!")

root = tk.Tk()
root.title("ASCII Video Converter")

input_var = tk.StringVar()
output_var = tk.StringVar(value="output.mp4")
mode_var = tk.StringVar(value="simple")
bg_var = tk.StringVar(value="white")
cols_var = tk.IntVar(value=100)
scale_var = tk.IntVar(value=1)
fps_var = tk.IntVar(value=0)
overlay_var = tk.DoubleVar(value=0.0)

tk.Label(root, text="Input Video:").grid(row=0, column=0)
tk.Entry(root, textvariable=input_var, width=40).grid(row=0, column=1)
tk.Button(root, text="Browse", command=select_input).grid(row=0, column=2)

tk.Label(root, text="Output Video:").grid(row=1, column=0)
tk.Entry(root, textvariable=output_var, width=40).grid(row=1, column=1)

tk.Label(root, text="Mode:").grid(row=2, column=0)
tk.OptionMenu(root, mode_var, "simple", "complex").grid(row=2, column=1)

tk.Label(root, text="Background:").grid(row=3, column=0)
tk.OptionMenu(root, bg_var, "white", "black").grid(row=3, column=1)

tk.Label(root, text="Num Columns:").grid(row=4, column=0)
tk.Entry(root, textvariable=cols_var).grid(row=4, column=1)

tk.Label(root, text="Scale:").grid(row=5, column=0)
tk.Entry(root, textvariable=scale_var).grid(row=5, column=1)

tk.Label(root, text="FPS (0 = original):").grid(row=6, column=0)
tk.Entry(root, textvariable=fps_var).grid(row=6, column=1)

tk.Label(root, text="Overlay Ratio:").grid(row=7, column=0)
tk.Entry(root, textvariable=overlay_var).grid(row=7, column=1)

tk.Button(root, text="Convert", command=run_conversion).grid(row=8, column=1)

root.mainloop()

