# Smart Clip ⚡

> Smart Clip is a lightweight, background-running system utility designed for developers, featuring automatic code snippet classification, instant search, and a sleek global hotkey HUD.

---

## ✨ Features

- 🎯 **Smart Code & Snippet Classification**: Automatically detects and tags copied content by category and programming language (Python, C++/C, Java, Rust, JavaScript, HTML, CSS, SQL, Bash, JSON, Logs, and Links).
- ⌨️ **Global Hotkey HUD**: Summon or close the HUD instantly from anywhere across your OS using `Ctrl + Shift + X`.
- 🔍 **Real-Time Search**: Filter through your clipboard history in real-time with an intuitive, built-in search bar.
- ⚡ **Featherlight Footprint**: Designed to run seamlessly in the background with minimal CPU and RAM usage.
- 🎨 **Modern Dark Theme**: Styled with a dark aesthetic, rounded cards, and color-coded language badges for developer productivity.

---

## 💻 Tech Stack

- **Python**
- **CustomTkinter** (Modern UI engine)
- **Pyperclip** (Cross-platform clipboard access)
- **Keyboard** (Global key hooks)
- **PyInstaller** (Executable packaging)

---

## 🛠️ Getting Started

### Option 1: Run as Executable (Recommended)

1. Download the latest `smart_clip.exe` from the [Releases](../../releases) section or project root.
2. Run `smart_clip.exe`. It will start silently in the background.
3. Press `Ctrl + Shift + X` to toggle the Smart Clip HUD.

---

### Option 2: Run from Source

#### Prerequisites
Ensure you have Python 3.10+ installed.

#### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/SmartClip.git
   cd SmartClip
   ```

2. Install the required packages:
   ```bash
   pip install customtkinter pyperclip keyboard pillow
   ```

3. Launch Smart Clip:
   ```bash
   python smart_clip.py
   ```

---

## ⌨️ Shortcuts & Controls

| Shortcut | Action |
| :--- | :--- |
| `Ctrl + Shift + X` | Toggle the Smart Clip HUD |
| `Escape` | Close the HUD |
| `Click on Card` | Copy snippet to clipboard & hide HUD |

---

## 📦 Building Executable from Source

To compile the standalone `.exe` without a console window:

```bash
pyinstaller --noconsole --onefile --icon=smartclip.png smart_clip.py
```

The output executable will be placed inside the `dist/` directory.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
