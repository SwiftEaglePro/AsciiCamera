# ASCII Camera

**Live macOS webcam footage converted into ASCII art directly in your terminal.**

Created by **SwiftEaglePro**

## Features

- Live webcam-to-ASCII conversion
- Five selectable ASCII styles
- Adjustable frame rate
- Automatic terminal-size adaptation
- Live FPS counter
- Simple keyboard controls
- Press `Q` to quit

## ASCII Styles

| Style | Description |
|---|---|
| Standard | Traditional ASCII shading |
| Detailed | Block characters |
| Matrix | Binary-style characters |
| Minimal | Simple character shading |
| Dense | High-density ASCII characters |

## Requirements

- macOS
- Python 3
- A connected or built-in camera
- Terminal camera permissions

## Installation

Clone the repository:

    git clone https://github.com/SwiftEaglePro/AsciiCamera.git
    cd AsciiCamera

Create and activate a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies:

    python -m pip install -r requirements.txt

## Usage

Start ASCII Camera:

    python ascii_camera.py

Choose an ASCII style from the menu.

Press `Q` to stop the camera.

## Project Structure

    AsciiCamera/
    ├── ascii_camera.py
    ├── requirements.txt
    ├── README.md
    ├── LICENSE
    └── .gitignore

## Creator

**SwiftEaglePro**

Version 1.1.0

Copyright © 2026 SwiftEaglePro.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.