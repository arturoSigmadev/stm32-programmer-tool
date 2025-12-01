# Unified STM32 Programmer

A comprehensive, unified tool for building, flashing, and deploying STM32 firmware projects. This tool consolidates functionality from multiple scripts into a single, cohesive Python package.

## 🎯 Features

- **Build**: Compile STM32 projects using STM32CubeIDE or GNU Make
- **Flash**: Program STM32 devices via STM32CubeProgrammer or OpenOCD
- **Deploy**: Combined build and flash operations in one command
- **Verify**: Automatic verification after flashing
- **Multi-Platform**: Works on Windows, Linux, and macOS
- **CLI & API**: Both command-line and Python API interfaces
- **Configuration**: Persistent settings management
- **GUI Support**: Legacy GUI mode available

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

```bash
# Clone the repository
git clone https://github.com/uqomm/sw-Stm32Programmer.git
cd sw-Stm32Programmer

# No additional installation required
python --version  # Verify Python 3.7+
```

## 🚀 Quick Start

### Command Line Usage

```bash
# Deploy (build + flash) - Most common use case
python -m cli.flash_cli deploy /path/to/project

# Deploy with clean build
python -m cli.flash_cli deploy /path/to/project --clean

# Flash only (skip build)
python -m cli.flash_cli flash /path/to/firmware.hex

# Build only
python -m cli.flash_cli build /path/to/project

# Erase chip
python -m cli.flash_cli erase

# Check programmer status
python -m cli.flash_cli status

# Configure settings
python -m cli.flash_cli settings --programmer STM32_Programmer_CLI
```

### Windows Batch Wrapper

```cmd
REM Use the convenient batch wrapper
scripts\flash_gateway.bat

REM Or with project path
scripts\flash_gateway.bat C:\path\to\project
```

### Python API Usage

```python
from core.deployer import STM32Deployer
from core.programmer import STM32Programmer
from core.builder import STM32Builder

# Deploy (build + flash)
deployer = STM32Deployer()
success = deployer.deploy_project(
    project_path="./project",
    clean_build=True,
    verify=True
)

# Flash only
programmer = STM32Programmer()
success = programmer.flash(
    firmware_path="firmware.hex",
    programmer_type="STM32_Programmer_CLI",
    verify=True
)

# Build only
builder = STM32Builder()
result = builder.build_project(
    project_path="./project",
    clean=True
)
```

## 📖 Documentation

### CLI Commands

#### `deploy`
Build and flash firmware in one operation.

```bash
python -m cli.flash_cli deploy <project_path> [options]

Options:
  --clean          Clean build before compiling
  --programmer     Programmer type (STM32_Programmer_CLI or openocd)
  --verify         Verify after flashing (default: enabled)
```

#### `flash`
Flash pre-built firmware to device.

```bash
python -m cli.flash_cli flash <firmware_path> [options]

Options:
  --programmer     Programmer type
  --verify         Verify after flashing
```

#### `build`
Build project without flashing.

```bash
python -m cli.flash_cli build <project_path> [options]

Options:
  --clean          Clean build
```

#### `erase`
Erase the entire chip.

```bash
python -m cli.flash_cli erase [options]

Options:
  --programmer     Programmer type
```

#### `status`
Check programmer connection and device status.

```bash
python -m cli.flash_cli status
```

#### `settings`
View or update persistent settings.

```bash
python -m cli.flash_cli settings [options]

Options:
  --programmer     Set default programmer
  --show           Display current settings
```

### Configuration

Settings are stored in `~/.stm32_programmer_config.json`:

```json
{
  "programmer_type": "STM32_Programmer_CLI",
  "verify_after_flash": true,
  "default_project_path": "/path/to/project",
  "last_used": "2025-12-01T10:00:00"
}
```

### Module Structure

```
sw-Stm32Programmer/
├── core/
│   ├── programmer.py    # STM32 flashing functionality
│   ├── builder.py       # Project building functionality
│   └── deployer.py      # Combined build+flash operations
├── cli/
│   └── flash_cli.py     # Command-line interface
├── config/
│   └── settings.py      # Configuration management
└── scripts/
    └── flash_gateway.bat # Windows batch wrapper
```

## 🔧 Advanced Usage

### Custom Build Systems

The tool auto-detects build systems but can be customized:

```python
from core.builder import STM32Builder, BuildSystem

builder = STM32Builder()

# Force specific build system
result = builder.build_project(
    project_path="./project",
    build_system=BuildSystem.MAKE
)
```

### Custom Programmer Settings

```python
from core.programmer import STM32Programmer, ProgrammerType

programmer = STM32Programmer()

# Use OpenOCD instead of STM32CubeProgrammer
success = programmer.flash(
    firmware_path="firmware.hex",
    programmer_type=ProgrammerType.OPENOCD
)
```

### Error Handling

```python
from core.deployer import STM32Deployer, DeploymentError

deployer = STM32Deployer()

try:
    success = deployer.deploy_project("./project")
    if success:
        print("✅ Deployment successful!")
except DeploymentError as e:
    print(f"❌ Deployment failed: {e}")
```

## 🐛 Troubleshooting

### Programmer Not Found

```bash
# Check if STM32CubeProgrammer is in PATH
python -m cli.flash_cli status

# If not found, install STM32CubeProgrammer or use OpenOCD
python -m cli.flash_cli settings --programmer openocd
```

### Build Failures

```bash
# Try clean build
python -m cli.flash_cli build ./project --clean

# Check if STM32CubeIDE or Make is available
which stm32cubeide  # Linux/Mac
where stm32cubeide  # Windows
```

### Connection Issues

- Verify ST-Link drivers are installed
- Check USB connection to STM32 device
- Ensure no other tools are using the programmer
- Try resetting the device

## 📝 Migration Guide

### From Old GUI Tool

The legacy GUI tool (`src/programmer.py`) is deprecated. Use the new CLI:

```bash
# Old way (deprecated)
python src/programmer.py

# New way (recommended)
python -m cli.flash_cli deploy ./project
```

### From Script-Based Workflow

```bash
# Old scripts (deprecated)
bash scripts/build/build.py
bash scripts/deploy/flash_gateway.py

# New unified tool
python -m cli.flash_cli deploy ./project
```

## 🤝 Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 style guidelines
- All functions have docstrings
- Changes are tested on Windows and Linux
- Update README for new features

## 📄 License

This project is licensed under the MIT License.

## 🔗 Related Projects

- [fw-gateway1Lora](https://github.com/uqomm/fw-gateway1Lora) - STM32F103 LoRa Gateway Firmware
- [sw-jiraanalysis](https://github.com/uqomm/sw-jiraanalysis) - Jira Analysis Tools

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation in `docs/`
- Review troubleshooting section above

---

**Version**: 3.0.0  
**Last Updated**: December 2025
