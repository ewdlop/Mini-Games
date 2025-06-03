# Chinese Python Games Builder for Windows

This guide explains how to build your Chinese Python games into Windows executables using the provided PowerShell script.

## 📋 Prerequisites

1. **Python 3.8+** installed on Windows
2. **PowerShell** (comes with Windows)
3. Your Chinese Python game files in the project directory

## 🎮 Supported Games

The script will automatically build these Chinese Python games:

- **貪食蛇.py** - Snake Game
- **六子棋.py** - Connect 6
- **計算機.py** - Calculator
- **掃地雷.py** - Minesweeper
- **數獨.py** - Sudoku
- **五子棋.py** - Gomoku/Five in a Row
- **四子棋.py** - Connect Four
- **圈圈叉叉.py** - Tic Tac Toe
- **そうこばん.py** - Sokoban

## 🚀 Quick Start

### Method 1: Using the Batch File (Easiest)

1. Open Command Prompt or File Explorer
2. Navigate to your project directory
3. Double-click `build-chinese-games.bat` or run:
   ```cmd
   build-chinese-games.bat
   ```

### Method 2: Using PowerShell Directly

1. Open PowerShell as Administrator (recommended)
2. Navigate to your project directory:
   ```powershell
   cd "C:\path\to\your\project"
   ```
3. Run the script:
   ```powershell
   .\build-chinese-games.ps1
   ```

## 🔧 Advanced Usage

### Command Line Parameters

```powershell
.\build-chinese-games.ps1 [parameters]
```

**Available Parameters:**

- `-PythonPath "C:\Python39"` - Specify custom Python installation path
- `-OutputDir "my-release"` - Change output directory (default: "release")
- `-Clean` - Clean the output directory before building
- `-Verbose` - Show detailed build output

**Examples:**

```powershell
# Basic build
.\build-chinese-games.ps1

# Clean build with custom output directory
.\build-chinese-games.ps1 -Clean -OutputDir "dist"

# Use specific Python installation
.\build-chinese-games.ps1 -PythonPath "C:\Python311"

# Verbose output for debugging
.\build-chinese-games.ps1 -Verbose
```

## 📁 Output Structure

After successful build, your release directory will look like this:

```
release/
├── 貪食蛇/
│   └── 貪食蛇.exe
├── 六子棋/
│   └── 六子棋.exe
├── 計算機/
│   └── 計算機.exe
├── 掃地雷/
│   └── 掃地雷.exe
└── ... (other games)
```

Each game gets its own directory with the executable file.

## 🛠️ What the Script Does

1. **Auto-detects Python** - Finds your Python installation automatically
2. **Installs PyInstaller** - Automatically installs if not present
3. **Installs dependencies** - Reads `requirements.txt` if available
4. **Builds executables** - Uses PyInstaller to create standalone .exe files
5. **Organizes output** - Places each game in its own directory
6. **Cleans up** - Removes temporary build files

## 🐛 Troubleshooting

### Common Issues

**1. "Python not found" Error**
```
Solution: Install Python from python.org or specify path with -PythonPath
```

**2. "PyInstaller installation failed" Error**
```
Solution: Run PowerShell as Administrator or update pip:
python -m pip install --upgrade pip
```

**3. "No Chinese Python game files found" Error**
```
Solution: Ensure you're in the correct directory with your .py files
```

**4. PowerShell Execution Policy Error**
```
Solution: Run as Administrator and set execution policy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**5. Chinese Character Display Issues**
```
Solution: The script uses --console flag to ensure proper character encoding
```

### Manual Debugging

If you need to debug a specific game build:

```powershell
# Build single game manually
python -m PyInstaller --onefile --console "貪食蛇.py"
```

## 📦 Dependencies

The script automatically handles:

- **PyInstaller** - For creating executables
- **Requirements** - Installs from requirements.txt if present
- **Python modules** - All imported modules in your games

## 🔒 Security Note

- The batch file temporarily sets PowerShell execution policy to Bypass for the build process
- This is safe and only affects the current PowerShell session
- Your system's global execution policy remains unchanged

## 📈 Performance Tips

- Use `-Clean` parameter periodically to remove old build artifacts
- Large games may take longer to build - this is normal
- The first build will be slower as it downloads and installs PyInstaller

## 🆘 Getting Help

If you encounter issues:

1. Run with `-Verbose` flag for detailed output
2. Check that all your Python files have the required dependencies
3. Ensure your Python installation is complete and functional
4. Try building games individually to isolate issues

## 🎯 Next Steps

After building:

1. Test each executable by running it
2. Distribute the entire game directories (not just the .exe files)
3. Consider creating a installer or zip package for distribution
4. Test on other Windows machines to ensure compatibility

---

**Happy Building! 🎮✨** 