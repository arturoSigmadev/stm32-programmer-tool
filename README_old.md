# Unified STM32 Programmer

A comprehensive, unified tool for building, flashing, and deploying STM32 firmware projects. This tool consolidates functionality from multiple scripts into a single, cohesive package.

## 🎯 Features

- **Build**: Compile STM32 projects using STM32CubeIDE or Make
- **Flash**: Program STM32 devices via SWD/ST-Link or OpenOCD
- **Deploy**: Combined build and flash operations in one command
- **Verify**: Automatic verification after flashing
- **Multi-Platform**: Works on Windows, Linux, and macOS
- **CLI & API**: Both command-line and Python API interfaces
- **Configuration**: Persistent settings management

## 📦 Installation

### Requirements

- Python 3.7 or later
- **One of the following** for flashing:
  - STM32CubeProgrammer (recommended)
  - OpenOCD
- **One of the following** for building:
  - STM32CubeIDE
  - GNU Make + ARM GCC toolchain

### Setup

No installation required - the tool works directly from the repository:

```bash
# Verify Python
python --version

# Check if STM32CubeProgrammer is available
python -m utils.stm32Programmer.cli.flash_cli status
```

## 🚀 Quick Start

### Command Line Usage

```bash
# Deploy (build + flash) - Most common use case
python -m utils.stm32Programmer.cli.flash_cli deploy ./project

# Deploy with clean build
python -m utils.stm32Programmer.cli.flash_cli deploy ./project --clean

# Flash only (skip build)
python -m utils.stm32Programmer.cli.flash_cli deploy ./project --no-build

# Flash a specific binary
python -m utils.stm32Programmer.cli.flash_cli flash firmware.bin

# Build only
python -m utils.stm32Programmer.cli.flash_cli build ./project --clean

# Erase device
python -m utils.stm32Programmer.cli.flash_cli erase --full

# Check status
python -m utils.stm32Programmer.cli.flash_cli status ./project
```

### Windows Batch Script (Legacy Compatibility)

```bat
REM Simple deployment
utils\stm32Programmer\scripts\flash_gateway.bat

REM Clean and rebuild
utils\stm32Programmer\scripts\flash_gateway.bat --clean

REM Flash only (skip build)
utils\stm32Programmer\scripts\flash_gateway.bat --no-build
```

### Python API Usage

```python
from pathlib import Path
from utils.stm32Programmer import STM32Config, STM32Deployer

# Configure
config = STM32Config(
    port="SWD",
    chip="STM32F103C8",
    verify=True,
    auto_reset=True
)

# Deploy (build + flash)
deployer = STM32Deployer(Path("./project"), config)
success = deployer.deploy(clean=True, verify=True)

if success:
    print("Deployment successful!")
```

## 📋 Command Reference

### Deploy Command

Build and flash firmware in one operation:

```bash
python -m utils.stm32Programmer.cli.flash_cli deploy <project_path> [options]

Options:
  --port SWD          Connection port (SWD, UART, USB)
  --chip STM32F103C8  Target chip
  --clean             Clean before building
  --no-build          Skip build step
  --config Debug      Build configuration (Debug/Release)
  --no-verify         Skip verification after flash
```

### Flash Command

Flash a pre-built binary:

```bash
python -m utils.stm32Programmer.cli.flash_cli flash <binary_file> [options]

Options:
  --port SWD          Connection port
  --chip STM32F103C8  Target chip
  --address 0x08000000  Flash start address
  --no-verify         Skip verification
```

### Build Command

Build firmware without flashing:

```bash
python -m utils.stm32Programmer.cli.flash_cli build <project_path> [options]

Options:
  --clean             Clean before building
  --config Debug      Build configuration (Debug/Release)
```

### Erase Command

Erase device flash memory:

```bash
python -m utils.stm32Programmer.cli.flash_cli erase [options]

Options:
  --port SWD          Connection port
  --full              Full chip erase (vs mass erase)
```

### Status Command

Show device and build information:

```bash
python -m utils.stm32Programmer.cli.flash_cli status [project_path] [options]

Options:
  --port SWD          Connection port
```

### Settings Command

Manage configuration:

```bash
# Show current settings
python -m utils.stm32Programmer.cli.flash_cli settings --show

# Set a value
python -m utils.stm32Programmer.cli.flash_cli settings --set default_port SWD

# Reset to defaults
python -m utils.stm32Programmer.cli.flash_cli settings --reset
```

## ⚙️ Configuration

Settings are stored in `~/.stm32programmer/config.json`:

```json
{
  "default_port": "SWD",
  "default_baudrate": 115200,
  "default_chip": "STM32F103C8",
  "stm32cube_path": null,
  "openocd_path": null,
  "verify_by_default": true,
  "auto_reset": true,
  "build_before_flash": true,
  "clean_before_build": false
}
```

## 🔄 Migration from Old Scripts

### Old Structure
```
scripts/
  deploy/
    flash_gateway.py
    flash_gateway.bat
    flash.py
  build/
    build.py
```

### New Unified Structure
```
utils/
  stm32Programmer/
    core/         # Core functionality
    cli/          # Command-line interface
    config/       # Configuration management
    scripts/      # Wrapper scripts
```

### Migration Examples

**Old:** `python scripts/deploy/flash_gateway.py`  
**New:** `python -m utils.stm32Programmer.cli.flash_cli deploy ./project`

**Old:** `python scripts/build/build.py`  
**New:** `python -m utils.stm32Programmer.cli.flash_cli build ./project`

**Old:** `scripts\deploy\flash_gateway.bat`  
**New:** `utils\stm32Programmer\scripts\flash_gateway.bat`

## 🏗️ Architecture

```
utils/stm32Programmer/
├── __init__.py              # Package initialization
├── core/
│   ├── programmer.py        # STM32 programming logic
│   ├── builder.py           # Build functionality
│   └── deployer.py          # Unified deployment
├── cli/
│   └── flash_cli.py         # Command-line interface
├── config/
│   └── settings.py          # Settings management
└── scripts/
    └── flash_gateway.bat    # Windows batch wrapper
```

## 🔧 Supported Hardware

- **STM32F1xx** series (F103, F107, etc.)
- **STM32F4xx** series  
- **STM32G4xx** series (G474, etc.)
- **STM32H7xx** series

## 🛠️ Troubleshooting

### Programmer Not Found

```bash
# Check if STM32CubeProgrammer is installed
STM32_Programmer_CLI --version

# Or install OpenOCD
sudo apt-get install openocd  # Linux
brew install openocd          # macOS
```

### Build Fails

```bash
# Check if Make is available
make --version

# Or use STM32CubeIDE headless build
# Ensure STM32CubeIDE is installed
```

### Connection Issues

```bash
# Check device connection
python -m utils.stm32Programmer.cli.flash_cli status

# Try different port
python -m utils.stm32Programmer.cli.flash_cli flash firmware.bin --port UART
```

## 📝 Examples

### Example 1: Standard Workflow

```bash
# Clean build and deploy
cd /path/to/fw-gateway1Lora
python -m utils.stm32Programmer.cli.flash_cli deploy ./project --clean
```

### Example 2: Quick Reflash

```bash
# Flash without rebuilding
python -m utils.stm32Programmer.cli.flash_cli deploy ./project --no-build
```

### Example 3: Custom Binary

```bash
# Flash a specific binary file
python -m utils.stm32Programmer.cli.flash_cli flash ./custom_firmware.bin \
    --address 0x08000000 \
    --chip STM32F103C8
```

### Example 4: Python Script Integration

```python
#!/usr/bin/env python3
from pathlib import Path
from utils.stm32Programmer import STM32Config, STM32Deployer

def deploy_gateway():
    """Deploy gateway firmware"""
    config = STM32Config(port="SWD", chip="STM32F103C8")
    deployer = STM32Deployer(Path("./project"), config)
    
    # Build and flash
    if deployer.deploy(clean=True):
        print("✓ Deployment successful")
        return 0
    else:
        print("✗ Deployment failed")
        return 1

if __name__ == "__main__":
    exit(deploy_gateway())
```

## 🤝 Contributing

This tool consolidates and improves upon previous implementations. When adding features:

1. Keep API backward compatible
2. Update both CLI and Python API
3. Add examples to this README
4. Test on multiple platforms

## 📄 License

Part of the fw-gateway1Lora project.

## 🔗 Related Documentation

- [STM32CubeProgrammer User Manual](https://www.st.com/en/development-tools/stm32cubeprog.html)
- [OpenOCD Documentation](https://openocd.org/doc/)
- [Project Main README](../../../README.md)

---

**Version:** 2.0.0  
**Last Updated:** December 2025
