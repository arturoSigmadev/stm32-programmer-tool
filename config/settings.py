"""
Configuration management for STM32 Programmer
Handles settings persistence and defaults
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class ProgrammerSettings:
    """Global programmer settings"""
    default_port: str = "SWD"
    default_baudrate: int = 115200
    default_chip: str = "STM32F103C8"
    stm32cube_path: Optional[str] = None
    openocd_path: Optional[str] = None
    verify_by_default: bool = True
    auto_reset: bool = True
    build_before_flash: bool = True
    clean_before_build: bool = False


class SettingsManager:
    """Manage programmer settings"""
    
    def __init__(self, config_file: Optional[Path] = None):
        """
        Initialize settings manager
        
        Args:
            config_file: Path to config file (default: ~/.stm32programmer/config.json)
        """
        if config_file is None:
            config_file = Path.home() / ".stm32programmer" / "config.json"
        
        self.config_file = Path(config_file)
        self.settings = self.load()
    
    def load(self) -> ProgrammerSettings:
        """
        Load settings from file
        
        Returns:
            ProgrammerSettings instance
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    return ProgrammerSettings(**data)
            except Exception as e:
                print(f"[WARNING] Failed to load settings: {e}")
                print("[INFO] Using default settings")
        
        return ProgrammerSettings()
    
    def save(self) -> bool:
        """
        Save settings to file
        
        Returns:
            True if successful
        """
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(asdict(self.settings), f, indent=2)
            return True
        except Exception as e:
            print(f"[ERROR] Failed to save settings: {e}")
            return False
    
    def update(self, **kwargs) -> bool:
        """
        Update settings
        
        Args:
            **kwargs: Settings to update
        
        Returns:
            True if successful
        """
        for key, value in kwargs.items():
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)
            else:
                print(f"[WARNING] Unknown setting: {key}")
        
        return self.save()
    
    def reset_to_defaults(self) -> bool:
        """
        Reset settings to defaults
        
        Returns:
            True if successful
        """
        self.settings = ProgrammerSettings()
        return self.save()
    
    def get(self, key: str) -> Any:
        """
        Get a setting value
        
        Args:
            key: Setting name
        
        Returns:
            Setting value or None
        """
        return getattr(self.settings, key, None)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert settings to dictionary
        
        Returns:
            Dictionary of settings
        """
        return asdict(self.settings)
