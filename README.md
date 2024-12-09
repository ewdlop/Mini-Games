# Mini-Games
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
