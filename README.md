# 🧹 NEATFREAK: Automated Desktop Organizer

![Python Version](https://img.shields.io/badge/python-3.x-blue?style=flat-square)
![Platform](https://img.shields.io/badge/platform-Windows-win?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

**NEATFREAK** is a robust, event-driven background daemon that automatically organizes your "Downloads" folder in real-time. 

Unlike basic scripts that just move files, NEATFREAK features **smart icon injection**, **Windows Toast Notifications**, and a **"Legacy Cleanup" protocol** that vacuums up clutter from previous failed organization attempts.

---

## ✨ Key Features

* **⚡ Real-Time Monitoring:** Uses the `watchdog` library to detect file changes instantly. Zero polling means zero CPU waste.
* **🎨 Visual Hacking:** Automatically injects native Windows system icons (Cameras, Film Strips, Musical Notes) into created folders for a polished aesthetic.
* **🔔 Toast Notifications:** Receive a slick Windows notification every time a file is sorted, telling you exactly where it went.
* **📂 Deep Nesting:** Sorts files into professional hierarchies:
    * `Media/Images`
    * `Dev/Code/Python`
    * `Docs/Financial/PDFs`
* **🧹 Legacy Cleanup:** Automatically detects and empties old clutter folders (`Archives`, `Installers`, etc.) and re-sorts their contents into the new system.
* **🛡️ Browser Safety:** Smartly ignores temporary browser files (`.crdownload`, `.tmp`) to prevent corruption during active downloads.

---

## 🚀 Getting Started

### Prerequisites
* **Python 3.x** installed on your machine.
* **Windows 10/11** (Required for Icon Injection and Notifications).

### Installation

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/GhxstOSINT/NEATFREAK.git](https://github.com/GhxstOSINT/NEATFREAK.git)
    cd NEATFREAK
    ```

2.  **Install Dependencies**
    NEATFREAK relies on lightweight libraries for monitoring and notifications.
    ```bash
    pip install watchdog plyer
    ```

---

## 📖 Usage

### Option 1: Live Monitoring (Terminal)
Run the script to see a live log of every action taken.
```bash
python neatfreak.py
Press Ctrl + C to stop.

Option 2: "Stealth Mode" (Background Service)
To run NEATFREAK silently in the background (perfect for startup):

Rename neatfreak.py to neatfreak.pyw.

Double-click the file. Nothing will appear on screen, but it is running.

To Stop: Open Task Manager, find pythonw.exe, and end the task.

⚙️ Configuration
The behavior of NEATFREAK is controlled entirely by config.json. You can modify this file to add your own rules without touching the code.

Example config.json:

JSON

{
    "watch_directory": "C:/Users/YourName/Downloads",
    "extension_map": {
        ".jpg": "Media/Images",
        ".mp4": "Media/Videos",
        ".py": "Dev/Code",
        ".exe": "Software/Installers"
    }
}
Unknown Files: Any file extension not listed in the config is automatically moved to an Others/ folder to keep your root directory clean.

🏗️ Project Structure
Plaintext

NEATFREAK/
├── config.json       # The brain: Rules and paths
├── neatfreak.py      # The engine: Monitoring logic
├── .gitignore        # Git rules (excludes cache)
└── README.md         # Documentation
⚠️ Troubleshooting
"Notification failed": Ensure "Focus Assist" or "Do Not Disturb" is turned off in Windows Settings.

"Icons not showing": Windows caches icons aggressively. If a folder icon doesn't update immediately, refresh the folder or restart Windows Explorer.

"Permission Denied": Ensure you are not trying to move a file that is currently open in another program.

🤝 Contributing
Contributions are welcome! If you have ideas for Linux/macOS support or new sorting algorithms:

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

Author
GhxstOSINT