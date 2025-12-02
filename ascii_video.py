import argparse
import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageOps


def get_args():
    parser = argparse.ArgumentParser("Image to ASCII")
    parser.add_argument("--input", type=str, required=True, help="Path to input video")
    parser.add_argument("--output", type=str, required=True, help="Path to output video")
    parser.add_argument("--mode", type=str, default="simple", choices=["simple", "complex"],
                        help="10 or 70 different characters")
    parser.add_argument("--background", type=str, default="white", choices=["black", "white"],
                        help="background color")
    parser.add_argument("--num_cols", type=int, default=100, help="ASCII character columns")
    parser.add_argument("--scale", type=int, default=1, help="scale up text size")
    parser.add_argument("--fps", type=int, default=0, help="Frames per second (0 = original)")
    parser.add_argument("--overlay_ratio", type=float, default=0.0, help="Overlay video on ASCII (0 = none)")
    return parser.parse_args()


def main(opt):
    # ASCII char set
    CHAR_LIST = '@%#*+=-:. ' if opt.mode == "simple" else \
        "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "

    bg_code = 255 if opt.background == "white" else 0

    # Load system font (Menlo)
    font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", size=int(10 * opt.scale))

    cap = cv2.VideoCapture(opt.input)
    if not cap.isOpened():
        print(f"❌ Cannot open video file: {opt.input}")
        return

    original_fps = cap.get(cv2.CAP_PROP_FPS)
    fps = original_fps if opt.fps == 0 else opt.fps
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    char_bbox = font.getbbox("A")
    char_width = char_bbox[2] - char_bbox[0]
    char_height = char_bbox[3] - char_bbox[1]

    cell_width = width / opt.num_cols
    cell_height = 2 * cell_width
    num_rows = int(height / cell_height)

    num_cols = opt.num_cols
    out_width = width
    out_height = height

    out = cv2.VideoWriter(
        opt.output,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (out_width, out_height)
    )

    num_chars = len(CHAR_LIST)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ascii_img = Image.new("L", (char_width * num_cols, char_height * num_rows), bg_code)
        draw = ImageDraw.Draw(ascii_img)

        for i in range(num_rows):
            line = ""
            for j in range(num_cols):
                y1 = int(i * cell_height)
                y2 = int(min((i + 1) * cell_height, height))
                x1 = int(j * cell_width)
                x2 = int(min((j + 1) * cell_width, width))
                cell = gray[y1:y2, x1:x2]
                if cell.size == 0:
                    char = " "
                else:
                    avg = int(np.mean(cell))
                    char = CHAR_LIST[min(int(avg * num_chars / 255), num_chars - 1)]
                line += char
            draw.text((0, i * char_height), line, fill=255 - bg_code, font=font)

        # Resize ASCII to match original video resolution
        ascii_frame = ascii_img.resize((width, height))
        ascii_frame_bgr = cv2.cvtColor(np.array(ascii_frame), cv2.COLOR_GRAY2BGR)

        if opt.overlay_ratio > 0:
            overlay = cv2.resize(frame, (int(width * opt.overlay_ratio), int(height * opt.overlay_ratio)))
            ascii_frame_bgr[-overlay.shape[0]:, -overlay.shape[1]:] = overlay

        out.write(ascii_frame_bgr)

    cap.release()
    out.release()
    print(f"✅ Done! Output saved to {opt.output}")


if __name__ == '__main__':
    main(get_args())

