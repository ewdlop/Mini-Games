# Mini-Games

[![Pylint](https://github.com/ewdlop/Mini-Games/actions/workflows/pylint.yml/badge.svg)](https://github.com/ewdlop/Mini-Games/actions/workflows/pylint.yml)
[![CodeQL](https://github.com/ewdlop/Mini-Games/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/ewdlop/Mini-Games/actions/workflows/github-code-scanning/codeql)
[![Build Windows](https://github.com/ewdlop/Mini-Games/actions/workflows/main-windows.yml/badge.svg)](https://github.com/ewdlop/Mini-Games/actions/workflows/main-windows.yml)
[![Build Ubuntu](https://github.com/ewdlop/Mini-Games/actions/workflows/main-ubuntu.yml/badge.svg)](https://github.com/ewdlop/Mini-Games/actions/workflows/main-ubuntu.yml)
[![Build macOS](https://github.com/ewdlop/Mini-Games/actions/workflows/main-macos.yml/badge.svg)](https://github.com/ewdlop/Mini-Games/actions/workflows/main-macos.yml)

## Description
This repository contains a collection of mini-games implemented in various programming languages, including both English and Chinese (Traditional/Simplified) games. The purpose of this repository is to provide examples of simple game implementations and to serve as a learning resource for those interested in game development.

## 🎮 Games Included

### Python Games (English)
1. **3D Effect Game** (`3d_game.py`) - 3D visual effects game
2. **Breakout** (`breakout.py`) - Classic brick-breaking game
3. **Crossword Puzzle Generator** (`crossword_puzzle_generator.py`) - Generate crossword puzzles
4. **OpenGL 3D Game** (`opengl_python_game.py`) - 3D game using OpenGL
5. **Pacman** (`pacman.py`) - Classic Pac-Man style game
6. **Ping Pong** (`ping_pong.py`) - Table tennis game
7. **Snake** (`snake.py`) - Classic snake game

### Python Games (Chinese/Japanese)
1. **貪食蛇** (`貪食蛇.py`) - Snake game in Chinese
2. **六子棋** (`六子棋.py`) - Connect Six game
3. **五子棋** (`五子棋.py`) - Gomoku/Five in a Row
4. **四子棋** (`四子棋.py`) - Connect Four
5. **圈圈叉叉** (`圈圈叉叉.py`) - Tic-Tac-Toe
6. **掃地雷** (`掃地雷.py`) - Minesweeper
7. **數獨** (`數獨.py`) - Sudoku
8. **そうこばん** (`そうこばん.py`) - Sokoban (Japanese)
9. **計算機** (`計算機.py`) - Calculator

### Other Games
1. **Arrow Key Beep** (`arrow-key.cs`) - C# console game
2. **Logic Gates Simulator** (`logic_gates.html`) - HTML/CSS logic simulator
3. **NAND Gate** (`NAND.html`) - NAND gate simulator
4. **Tetris** (`tetris-game (1).html`) - HTML/JavaScript Tetris
5. **15 Puzzle** (`16/Schylling 15 Puzzel.py`) - Sliding puzzle game

## 🚀 Quick Start

### Download Pre-built Executables
Check the [Releases](https://github.com/ewdlop/Mini-Games/releases) section for pre-built executables for Windows, macOS, and Linux.

### Run from Source

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ewdlop/Mini-Games.git
   cd Mini-Games
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run any game:**
   ```bash
   python pacman.py
   python 貪食蛇.py
   python 計算機.py
   ```

## 🔧 Building Executables

### Automated Builds
This repository includes GitHub Actions workflows that automatically build executables for Windows, macOS, and Linux when version tags are pushed:

- **Windows**: `main-windows.yml` - Builds `.exe` files using PyInstaller
- **Ubuntu**: `main-ubuntu.yml` - Builds Linux executables  
- **macOS**: `main-macos.yml` - Builds macOS executables

### Manual Build
You can also build executables manually using the provided scripts:

#### Windows PowerShell
```powershell
.\build-chinese-games.ps1
```

#### Windows Batch
```batch
build-chinese-games.bat
```

#### Using PyInstaller Directly
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole your_game.py
```

## 📁 Repository Structure

```
Mini-Games/
├── English Games/
│   ├── pacman.py
│   ├── ping_pong.py
│   ├── breakout.py
│   └── ...
├── Chinese/Japanese Games/
│   ├── 貪食蛇.py (Snake)
│   ├── 六子棋.py (Connect Six)
│   ├── 計算機.py (Calculator)
│   └── ...
├── Web Games/
│   ├── logic_gates.html
│   ├── tetris-game.html
│   └── ...
├── Build Scripts/
│   ├── build-chinese-games.ps1
│   ├── build-chinese-games.bat
│   └── requirements.txt
├── Release Executables/
│   └── release/
└── CI/CD Workflows/
    └── .github/workflows/
```

## 🎯 Game Categories

### Strategy Games
- **六子棋** (Connect Six) - Advanced connect game
- **五子棋** (Gomoku) - Five in a row
- **四子棋** (Connect Four) - Classic connect four

### Puzzle Games  
- **數獨** (Sudoku) - Number puzzle game
- **掃地雷** (Minesweeper) - Mine detection game
- **そうこばん** (Sokoban) - Box pushing puzzle

### Action Games
- **貪食蛇** (Snake) - Classic snake game
- **Pacman** - Maze chase game
- **Breakout** - Brick breaking game

### Utility Games
- **計算機** (Calculator) - Graphical calculator
- **Crossword Puzzle Generator** - Create crossword puzzles

## 🛠️ Requirements

### Python Games
- Python 3.7+
- pygame
- numpy (for some games)
- tkinter (usually included with Python)

### Web Games
- Modern web browser with HTML5 support

### C# Games
- .NET Framework or .NET Core
- Visual Studio or compatible C# compiler

## 🚀 Installation & Setup

1. **Install Python dependencies:**
   ```bash
   pip install pygame numpy
   ```

2. **For development with all dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run games directly:**
   ```bash
   python [game_name].py
   ```

## 🤝 Contributing
Contributions are welcome! If you have a mini-game you'd like to add or improvements to existing games, please follow these steps:

1. **Fork the repository**
2. **Create a new branch** for your feature or bugfix
3. **Make your changes** and commit them with descriptive messages  
4. **Push your changes** to your forked repository
5. **Create a pull request** to merge your changes into the main repository

Please ensure your code follows the existing style and includes comments where necessary.

### Guidelines for Contributors

- **Code Style**: Follow PEP 8 for Python code
- **Documentation**: Include docstrings and comments
- **Testing**: Test your games thoroughly before submitting
- **Localization**: Consider adding games in different languages
- **Dependencies**: Keep external dependencies minimal

## 📦 Releases

Pre-built executables are automatically generated for each release and are available in the [Releases](https://github.com/ewdlop/Mini-Games/releases) section. The automated build system creates executables for:

- **Windows** (.exe files)
- **macOS** (macOS executables) 
- **Linux** (Linux executables)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔒 Security

Please review our [Security Policy](SECURITY.md) for information about reporting security vulnerabilities.

## 🏗️ Build Information

For detailed build instructions and troubleshooting, see [BUILD_GUIDE.md](BUILD_GUIDE.md).

### Build Requirements

- **Python 3.7+**
- **PyInstaller** for creating executables
- **Required packages** listed in `requirements.txt`

### Automated Builds

The repository uses GitHub Actions for continuous integration:

- **Linting**: Code quality checks with Pylint
- **Security**: CodeQL security analysis  
- **Multi-platform builds**: Windows, macOS, and Linux executable generation

## 🌟 Featured Games

### Traditional Chinese Games
- **貪食蛇** - A beautifully implemented snake game with Chinese UI
- **六子棋** - Strategic Connect Six game
- **數獨** - Sudoku puzzle with intuitive interface

### Classic Arcade Games  
- **Pacman** - Full-featured Pac-Man implementation
- **Breakout** - Classic brick-breaking gameplay
- **Ping Pong** - Two-player table tennis

---

**Made with ❤️ by the Mini-Games community**

