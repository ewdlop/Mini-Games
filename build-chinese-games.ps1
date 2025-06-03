# Build Chinese Python Games for Windows
# This script builds Chinese Python game files into Windows executables
# and organizes them in a release directory

param(
    [string]$PythonPath = "",
    [string]$OutputDir = "release",
    [switch]$Clean = $false,
    [switch]$Verbose = $false
)

# Function to write colored output
function Write-ColorOutput($Message, $Color = "White") {
    Write-Host $Message -ForegroundColor $Color
}

# Function to check if Python is available
function Test-PythonInstallation {
    if ($PythonPath -ne "") {
        $pythonExe = Join-Path $PythonPath "python.exe"
        if (Test-Path $pythonExe) {
            return $pythonExe
        }
    }
    
    # Try to find Python in PATH
    try {
        $pythonCmd = cmd /c "where python" 2>$null
        if ($LASTEXITCODE -eq 0 -and $pythonCmd) {
            return $pythonCmd.Split([Environment]::NewLine)[0]
        }
    }
    catch {
        # Python not found in PATH
    }
    
    # Try common Python installation paths
    $commonPaths = @(
        "$env:LOCALAPPDATA\Programs\Python\Python*\python.exe",
        "$env:PROGRAMFILES\Python*\python.exe",
        "$env:PROGRAMFILES(x86)\Python*\python.exe",
        "C:\Python*\python.exe"
    )
    
    foreach ($pattern in $commonPaths) {
        $found = Get-ChildItem $pattern -ErrorAction SilentlyContinue | Sort-Object Name -Descending | Select-Object -First 1
        if ($found) {
            return $found.FullName
        }
    }
    
    return $null
}

# Function to install PyInstaller if not available
function Install-PyInstaller($PythonExe) {
    Write-ColorOutput "Checking PyInstaller installation..." "Yellow"
    
    $result = & $PythonExe -m pip show pyinstaller 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-ColorOutput "PyInstaller not found. Installing..." "Yellow"
        & $PythonExe -m pip install pyinstaller
        if ($LASTEXITCODE -ne 0) {
            Write-ColorOutput "Failed to install PyInstaller!" "Red"
            exit 1
        }
        Write-ColorOutput "PyInstaller installed successfully!" "Green"
    } else {
        Write-ColorOutput "PyInstaller is already installed." "Green"
    }
}

# Function to install requirements if requirements.txt exists
function Install-Requirements($PythonExe) {
    if (Test-Path "requirements.txt") {
        Write-ColorOutput "Installing requirements from requirements.txt..." "Yellow"
        & $PythonExe -m pip install -r requirements.txt
        if ($LASTEXITCODE -ne 0) {
            Write-ColorOutput "Warning: Some requirements failed to install." "Yellow"
        } else {
            Write-ColorOutput "Requirements installed successfully!" "Green"
        }
    }
}

# Function to build a single Python file
function Build-PythonGame($PythonExe, $GameFile, $OutputDir) {
    $gameName = [System.IO.Path]::GetFileNameWithoutExtension($GameFile)
    $gameDir = Join-Path $OutputDir $gameName
    
    Write-ColorOutput "Building: $GameFile -> $gameDir" "Cyan"
    
    # Create output directory for this game
    if (!(Test-Path $gameDir)) {
        New-Item -ItemType Directory -Path $gameDir -Force | Out-Null
    }
    
    # PyInstaller command
    $pyinstallerArgs = @(
        "--onefile",
        "--distpath", $gameDir,
        "--workpath", (Join-Path $gameDir "build"),
        "--specpath", (Join-Path $gameDir "spec"),
        "--name", $gameName,
        $GameFile
    )
    
    if (!$Verbose) {
        $pyinstallerArgs += "--log-level", "WARN"
    }
    
    # Add console flag for Chinese character support
    $pyinstallerArgs += "--console"
    
    # Run PyInstaller
    & $PythonExe -m PyInstaller @pyinstallerArgs
    
    if ($LASTEXITCODE -eq 0) {
        Write-ColorOutput "✓ Successfully built: $gameName" "Green"
        
        # Clean up build artifacts
        $buildDir = Join-Path $gameDir "build"
        $specDir = Join-Path $gameDir "spec"
        if (Test-Path $buildDir) { Remove-Item $buildDir -Recurse -Force }
        if (Test-Path $specDir) { Remove-Item $specDir -Recurse -Force }
        
        return $true
    } else {
        Write-ColorOutput "✗ Failed to build: $gameName" "Red"
        return $false
    }
}

# Main script execution
Write-ColorOutput "=== Chinese Python Games Builder ===" "Magenta"
Write-ColorOutput "Building Chinese Python games for Windows..." "White"

# Check Python installation
Write-ColorOutput "Searching for Python installation..." "Yellow"
$pythonExe = Test-PythonInstallation
if (!$pythonExe) {
    Write-ColorOutput "Python not found! Please install Python or specify the path with -PythonPath parameter." "Red"
    exit 1
}

Write-ColorOutput "Found Python: $pythonExe" "Green"

# Get Python version
$pythonVersion = & $pythonExe --version 2>&1
Write-ColorOutput "Python Version: $pythonVersion" "Green"

# Clean output directory if requested
if ($Clean -and (Test-Path $OutputDir)) {
    Write-ColorOutput "Cleaning output directory: $OutputDir" "Yellow"
    Remove-Item $OutputDir -Recurse -Force
}

# Create output directory
if (!(Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

# Install PyInstaller and requirements
Install-PyInstaller $pythonExe
Install-Requirements $pythonExe

# Define Chinese Python game files
$chineseGames = @(
    "貪食蛇.py",      # Snake
    "六子棋.py",      # Connect 6
    "計算機.py",      # Calculator
    "掃地雷.py",      # Minesweeper
    "數獨.py",        # Sudoku
    "五子棋.py",      # Gomoku/Five in a Row
    "四子棋.py",      # Connect Four
    "圈圈叉叉.py",    # Tic Tac Toe
    "そうこばん.py"   # Sokoban (Japanese but included)
)

# Find existing Chinese game files
$foundGames = @()
foreach ($game in $chineseGames) {
    if (Test-Path $game) {
        $foundGames += $game
    }
}

if ($foundGames.Count -eq 0) {
    Write-ColorOutput "No Chinese Python game files found!" "Red"
    Write-ColorOutput "Expected files: $($chineseGames -join ', ')" "Yellow"
    exit 1
}

Write-ColorOutput "Found $($foundGames.Count) Chinese game files:" "Green"
foreach ($game in $foundGames) {
    Write-ColorOutput "  - $game" "White"
}

# Build each game
$successCount = 0
$totalCount = $foundGames.Count

Write-ColorOutput "`nStarting build process..." "Yellow"

foreach ($game in $foundGames) {
    Write-ColorOutput "`n--- Building $game ---" "Cyan"
    
    if (Build-PythonGame $pythonExe $game $OutputDir) {
        $successCount++
    }
}

# Summary
Write-ColorOutput "`n=== Build Summary ===" "Magenta"
Write-ColorOutput "Successfully built: $successCount/$totalCount games" "Green"
Write-ColorOutput "Output directory: $OutputDir" "White"

if ($successCount -eq $totalCount) {
    Write-ColorOutput "All games built successfully! 🎉" "Green"
    
    # List built executables
    Write-ColorOutput "`nBuilt executables:" "Yellow"
    Get-ChildItem $OutputDir -Recurse -Filter "*.exe" | ForEach-Object {
        $relativePath = $_.FullName.Replace((Get-Location).Path + "\", "")
        Write-ColorOutput "  - $relativePath" "White"
    }
} else {
    Write-ColorOutput "Some games failed to build. Check the output above for details." "Yellow"
    exit 1
}

Write-ColorOutput "`nBuild completed!" "Green" 