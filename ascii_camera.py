import cv2
import numpy as np
import sys
import time
import shutil
import select
import tty
import termios

# ==========================================
#              ASCII CAMERA
# ==========================================
# Version: 1.1.0
#
# Created by: swifteagle
# Developer: swifteagle
# Copyright (c) 2026 swifteagle
#
# Python 3.15
# ==========================================

# Activate the venv:
# source .venv/bin/activate

# ==========================================
# ASCII STYLES
# ==========================================

STYLES = {
    "standard": "@%#*+=-:. ",
    "detailed": "█▓▒░ ",
    "matrix": "01 ",
    "minimal": "#:. ",
    "dense": "$@B%8&WM#*oahkbdpq"
}

STYLE_NAMES = {
    "1": "standard",
    "2": "detailed",
    "3": "matrix",
    "4": "minimal",
    "5": "dense"
}

FPS = 20
CAMERA_INDEX = 0


def select_style():

    print("\nChoose your ASCII style:")
    print("----------------------------------------")
    print("1. Standard")
    print("2. Detailed")
    print("3. Matrix")
    print("4. Minimal")
    print("5. Dense")
    print("----------------------------------------")

    while True:

        style = input("\nStyle: ").strip().lower()

        style = STYLE_NAMES.get(style, style)

        if style in STYLES:
            print(f"\nSelected style: {style.title()}")
            return STYLES[style]

        print("Invalid choice. Enter 1-5 or a style name.")


def frame_to_ascii(frame, width, height, ascii_chars):

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Correct for terminal character proportions
    resized = cv2.resize(
        gray,
        (width, height * 2),
        interpolation=cv2.INTER_AREA
    )

    # Average every two vertical pixels
    resized = resized.reshape(height, 2, width).mean(axis=1)

    # Convert brightness to ASCII
    indices = (
        resized / 255 * (len(ascii_chars) - 1)
    ).astype(int)

    return "\n".join(
        "".join(ascii_chars[i] for i in row)
        for row in indices
    )


def main():

    # ==========================================
    # STARTUP SCREEN
    # ==========================================

    print("=" * 40)
    print("              ASCII CAMERA")
    print("=" * 40)
    print("       Created by: swifteagle")
    print("          Developer: swifteagle")
    print("              Version 1.1.0")
    print("       Copyright (c) 2026")
    print("=" * 40)

    # Ask user for style
    ascii_chars = select_style()

    print("\nInitializing camera...")
    time.sleep(1)

    # ==========================================
    # CAMERA INITIALIZATION
    # ==========================================

    camera = cv2.VideoCapture(
        CAMERA_INDEX,
        cv2.CAP_AVFOUNDATION
    )

    if not camera.isOpened():
        print("\nERROR: Could not open camera.")
        print("Check macOS Camera permissions for Terminal.")
        return

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())

    print("\033[2J\033[?25l", end="")

    # Actual displayed FPS calculation
    frame_count = 0
    fps_start = time.time()
    current_fps = 0.0

    try:

        while True:

            start = time.time()

            width, height = shutil.get_terminal_size(
                (100, 40)
            )

            # Reserve space for status line
            height = max(1, height - 2)

            success, frame = camera.read()

            if not success:
                continue

            # Convert camera frame
            ascii_frame = frame_to_ascii(
                frame,
                width,
                height,
                ascii_chars
            )

            # Calculate actual FPS over time
            frame_count += 1
            elapsed_total = time.time() - fps_start

            if elapsed_total >= 1.0:
                current_fps = frame_count / elapsed_total
                frame_count = 0
                fps_start = time.time()

            # Update terminal
            sys.stdout.write("\033[H")
            sys.stdout.write(ascii_frame)

            sys.stdout.write(
                f"\n ASCII CAMERA | FPS: {current_fps:.1f} "
                f"| STYLE: {ascii_chars[:8]} | Q = Quit"
            )

            sys.stdout.flush()

            # Check keyboard
            ready, _, _ = select.select(
                [sys.stdin], [], [], 0
            )

            if ready:
                key = sys.stdin.read(1).lower()

                if key == "q":
                    break

            # FPS control
            elapsed = time.time() - start

            time.sleep(
                max(0, 1 / FPS - elapsed)
            )

    except KeyboardInterrupt:
        pass

    finally:

        camera.release()

        termios.tcsetattr(
            sys.stdin,
            termios.TCSADRAIN,
            old_settings
        )

        print("\033[?25h\033[0m")
        print("\nCamera stopped.")
        print("ASCII CAMERA - Created by swifteagle")


if __name__ == "__main__":
    main()