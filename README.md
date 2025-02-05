# Mini-Games

[![CodeQL](https://github.com/ewdlop/Mini-Games/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/ewdlop/Mini-Games/actions/workflows/github-code-scanning/codeql)

## Description
This repository contains a collection of mini-games implemented in various programming languages. The purpose of this repository is to provide examples of simple game implementations and to serve as a learning resource for those interested in game development.

## Games Included
1. 3D Effect Game (Python)
2. Arrow Key Beep (C#)
3. Breakout (Python)
4. Connect5 (Python)
5. Crossword Puzzle Generator (Python)
6. Logic Gates Simulator (HTML/CSS)
7. OpenGL 3D Game (Python)
8. Pacman (Python)
9. Ping Pong (Python)
10. Tetris (HTML/JavaScript)

## How to Run Each Game

### 3D Effect Game (Python)
1. Ensure you have Python and Pygame installed.
2. Run the `3d_game.py` script using Python.

### Arrow Key Beep (C#)
1. Open the `arrow-key.cs` file in a C# development environment (e.g., Visual Studio).
2. Compile and run the program.

### Breakout (Python)
1. Ensure you have Python and Pygame installed.
2. Run the `breakout.py` script using Python.

### Connect5 (Python)
1. Ensure you have Python and NumPy installed.
2. Run the `import numpy as np.py` script using Python.

### Crossword Puzzle Generator (Python)
1. Ensure you have Python installed.
2. Run the `crossword_puzzle_generator.py` script using Python.

### Logic Gates Simulator (HTML/CSS)
1. Open the `logic_gates.html` file in a web browser.

### OpenGL 3D Game (Python)
1. Ensure you have Python, Pygame, and PyOpenGL installed.
2. Run the `opengl_python_game.py` script using Python.

### Pacman (Python)
1. Ensure you have Python and Pygame installed.
2. Run the `pacman.py` script using Python.

### Ping Pong (Python)
1. Ensure you have Python and Pygame installed.
2. Run the `ping_pong.py` script using Python.

### Tetris (HTML/JavaScript)
1. Open the `tetris-game.html` file in a web browser.

## Contributing
Contributions are welcome! If you have a mini-game you'd like to add or improvements to existing games, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your forked repository.
5. Create a pull request to merge your changes into the main repository.

Please ensure your code follows the existing style and includes comments where necessary.

# Mini-Games
To build a Python executable, you can use tools like **PyInstaller**, **cx_Freeze**, or **Py2exe**. These tools package your Python script into a standalone executable that can be run on systems without requiring Python to be installed. Here's how you can do it using **PyInstaller**, one of the most popular options:

---

### Steps to Build a Python Executable Using PyInstaller

#### 1. **Install PyInstaller**
First, ensure PyInstaller is installed. Open your terminal or command prompt and run:
```bash
pip install pyinstaller
```

#### 2. **Navigate to Your Script Directory**
Change to the directory containing your Python script. For example:
```bash
cd path/to/your/script
```

#### 3. **Create the Executable**
Run PyInstaller with the desired options. The simplest command is:
```bash
pyinstaller your_script.py
```
This creates a folder named `dist` containing the executable.

#### 4. **Optional: Customize the Build**
You can customize how the executable is built by adding flags:
- **Single File Executable**: Create a single file instead of a folder:
  ```bash
  pyinstaller --onefile your_script.py
  ```
- **Add an Icon**: Specify an icon file for your executable:
  ```bash
  pyinstaller --onefile --icon=your_icon.ico your_script.py
  ```
- **Hide the Console** (for GUI apps): Prevent the console from opening when the executable is run:
  ```bash
  pyinstaller --onefile --noconsole your_script.py
  ```

#### 5. **Locate the Executable**
After running PyInstaller, your executable will be in the `dist` folder. For example:
```
dist/
  your_script.exe
```

#### 6. **Test the Executable**
Run the generated `.exe` file to ensure it works as expected.

---

### Additional Notes

- **Cross-Platform**: PyInstaller needs to be run on the same platform you are targeting (e.g., run it on Windows to generate a Windows executable).
- **Dependencies**: Ensure all required dependencies are installed in your Python environment.
- **Executable Size**: The size of the executable can be large because Python runtime and dependencies are bundled in.

---

### Example Command
```bash
pyinstaller --onefile --noconsole --icon=myicon.ico myscript.py
```

This creates a single-file executable with a custom icon and hides the console.

