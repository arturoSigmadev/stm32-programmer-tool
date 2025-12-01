"""
Unified STM32 Programmer Package
Integrates building, flashing, and deployment for STM32 projects
"""

__version__ = "2.0.0"
__author__ = "UQOMM Development Team"

from .core.programmer import STM32Programmer, STM32Config
from .core.builder import STM32Builder
from .core.deployer import STM32Deployer
from .config.settings import ProgrammerSettings, SettingsManager

__all__ = [
    "STM32Programmer",
    "STM32Config",
    "STM32Builder",
    "STM32Deployer",
    "ProgrammerSettings",
    "SettingsManager",
]
