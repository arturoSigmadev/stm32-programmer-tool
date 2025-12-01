"""
STM32 Programmer - Core Programming Logic
Handles flashing, erasing, and memory operations for STM32 devices
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from typing import Optional, List, Dict, Union
from dataclasses import dataclass


@dataclass
class STM32Config:
    """Configuration for STM32 programming operations"""
    port: str = "SWD"  # SWD, UART, USB
    baudrate: int = 115200
    chip: str = "STM32F103C8"
    flash_start: int = 0x08000000
    verify: bool = True
    auto_reset: bool = True
    
    # Optional programmer paths
    stm32cube_path: Optional[Path] = None
    openocd_path: Optional[Path] = None


class STM32Programmer:
    """Unified STM32 Programming Tool"""
    
    def __init__(self, config: STM32Config):
        self.config = config
        self.stm32_cli_path = None
        self.openocd_path = None
        self.use_openocd = False
        
        # Try to find programming tools
        self._find_programming_tools()
    
    def _find_programming_tools(self) -> None:
        """Locate STM32 programming tools"""
        # Try STM32CubeProgrammer first
        self.stm32_cli_path = self._find_stm32_programmer()
        
        # If not found, try OpenOCD
        if not self.stm32_cli_path:
            self.openocd_path = self._find_openocd()
            if self.openocd_path:
                self.use_openocd = True
                print(f"[INFO] Using OpenOCD: {self.openocd_path}")
        else:
            print(f"[INFO] Using STM32CubeProgrammer: {self.stm32_cli_path}")
    
    def _find_stm32_programmer(self) -> Optional[Path]:
        """Locate STM32_Programmer_CLI executable"""
        if self.config.stm32cube_path and self.config.stm32cube_path.exists():
            return self.config.stm32cube_path
        
        possible_paths = []
        
        if platform.system() == "Windows":
            possible_paths = [
                Path(r"C:\Program Files\STMicroelectronics\STM32Cube\STM32CubeProgrammer\bin\STM32_Programmer_CLI.exe"),
                Path(r"C:\Program Files (x86)\STMicroelectronics\STM32Cube\STM32CubeProgrammer\bin\STM32_Programmer_CLI.exe"),
                Path(r"C:\ST\STM32CubeIDE_1.11.0\STM32CubeIDE\plugins") / "**" / "STM32_Programmer_CLI.exe",
            ]
        else:  # Linux/macOS
            possible_paths = [
                Path("/usr/local/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI"),
                Path.home() / "STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI",
            ]
        
        for path in possible_paths:
            if path.exists():
                return path
            # Handle glob patterns
            if "**" in str(path):
                parent = Path(str(path).split("**")[0])
                pattern = str(path).split("**")[1].strip("/\\")
                if parent.exists():
                    matches = list(parent.rglob(pattern))
                    if matches:
                        return matches[0]
        
        return None
    
    def _find_openocd(self) -> Optional[Path]:
        """Locate OpenOCD executable"""
        if self.config.openocd_path and self.config.openocd_path.exists():
            return self.config.openocd_path
        
        # Try system PATH
        try:
            result = subprocess.run(["openocd", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return Path("openocd")
        except FileNotFoundError:
            pass
        
        return None
    
    def flash(self, binary_path: Union[Path, str], 
             address: Optional[int] = None,
             verify: Optional[bool] = None) -> bool:
        """
        Flash binary to STM32 device
        
        Args:
            binary_path: Path to binary file (.bin, .hex, .elf)
            address: Flash start address (default: from config)
            verify: Verify after flashing (default: from config)
        
        Returns:
            True if successful, False otherwise
        """
        binary_path = Path(binary_path)
        
        if not binary_path.exists():
            print(f"[ERROR] Binary file not found: {binary_path}")
            return False
        
        address = address if address is not None else self.config.flash_start
        verify = verify if verify is not None else self.config.verify
        
        print(f"\n{'='*60}")
        print(f"  Flashing {binary_path.name} to {self.config.chip}")
        print(f"{'='*60}\n")
        
        if self.use_openocd:
            return self._flash_with_openocd(binary_path, address, verify)
        else:
            return self._flash_with_stm32cube(binary_path, address, verify)
    
    def _flash_with_stm32cube(self, binary_path: Path, 
                             address: int, verify: bool) -> bool:
        """Flash using STM32CubeProgrammer"""
        if not self.stm32_cli_path:
            print("[ERROR] STM32CubeProgrammer not found")
            return False
        
        cmd = [
            str(self.stm32_cli_path),
            "-c", f"port={self.config.port}",
            "-w", str(binary_path), f"{hex(address)}",
        ]
        
        if verify:
            cmd.extend(["-v", str(binary_path), f"{hex(address)}"])
        
        if self.config.auto_reset:
            cmd.append("-rst")
        
        print(f"[INFO] Executing: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"\n[SUCCESS] ✓ Flashing completed successfully!")
                return True
            else:
                print(f"\n[ERROR] ✗ Flashing failed!")
                print(f"Error: {result.stderr}")
                return False
        except Exception as e:
            print(f"[ERROR] Exception during flashing: {e}")
            return False
    
    def _flash_with_openocd(self, binary_path: Path, 
                           address: int, verify: bool) -> bool:
        """Flash using OpenOCD"""
        if not self.openocd_path:
            print("[ERROR] OpenOCD not found")
            return False
        
        # Determine target config based on chip
        chip_lower = self.config.chip.lower()
        if "f103" in chip_lower:
            target = "stm32f1x.cfg"
        elif "f4" in chip_lower:
            target = "stm32f4x.cfg"
        elif "g4" in chip_lower:
            target = "stm32g4x.cfg"
        else:
            target = "stm32f1x.cfg"  # default
        
        # Determine interface
        interface = "stlink.cfg" if self.config.port == "SWD" else "jlink.cfg"
        
        cmd = [
            str(self.openocd_path),
            "-f", f"interface/{interface}",
            "-f", f"target/{target}",
            "-c", "init",
            "-c", "halt",
            "-c", f"program {binary_path} {hex(address)} {'verify' if verify else ''}",
            "-c", "reset" if self.config.auto_reset else "",
            "-c", "exit"
        ]
        
        # Remove empty commands
        cmd = [c for c in cmd if c]
        
        print(f"[INFO] Executing: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"\n[SUCCESS] ✓ Flashing completed successfully!")
                return True
            else:
                print(f"\n[ERROR] ✗ Flashing failed!")
                print(f"Error: {result.stderr}")
                return False
        except Exception as e:
            print(f"[ERROR] Exception during flashing: {e}")
            return False
    
    def erase(self, full: bool = False) -> bool:
        """
        Erase STM32 flash memory
        
        Args:
            full: Perform full chip erase (True) or mass erase (False)
        
        Returns:
            True if successful
        """
        print(f"\n[INFO] Erasing flash memory ({'full' if full else 'mass'})...")
        
        if self.use_openocd:
            return self._erase_with_openocd(full)
        else:
            return self._erase_with_stm32cube(full)
    
    def _erase_with_stm32cube(self, full: bool) -> bool:
        """Erase using STM32CubeProgrammer"""
        if not self.stm32_cli_path:
            print("[ERROR] STM32CubeProgrammer not found")
            return False
        
        cmd = [
            str(self.stm32_cli_path),
            "-c", f"port={self.config.port}",
            "-e", "all" if full else "0",
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print("[SUCCESS] ✓ Erase completed")
                return True
            else:
                print(f"[ERROR] ✗ Erase failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"[ERROR] Exception during erase: {e}")
            return False
    
    def _erase_with_openocd(self, full: bool) -> bool:
        """Erase using OpenOCD"""
        # Implement OpenOCD erase if needed
        print("[WARNING] OpenOCD erase not implemented yet")
        return False
    
    def read_memory(self, address: int, size: int, 
                   output_file: Path) -> bool:
        """
        Read memory from STM32 device
        
        Args:
            address: Start address
            size: Number of bytes to read
            output_file: Output file path
        
        Returns:
            True if successful
        """
        print(f"\n[INFO] Reading memory from {hex(address)}, size={size} bytes...")
        
        if not self.stm32_cli_path:
            print("[ERROR] STM32CubeProgrammer not found")
            return False
        
        cmd = [
            str(self.stm32_cli_path),
            "-c", f"port={self.config.port}",
            "-r", str(output_file), f"{hex(address)}", f"{hex(size)}",
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"[SUCCESS] ✓ Memory read to {output_file}")
                return True
            else:
                print(f"[ERROR] ✗ Read failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"[ERROR] Exception during read: {e}")
            return False
    
    def get_device_info(self) -> Optional[Dict[str, str]]:
        """Get connected device information"""
        if not self.stm32_cli_path:
            return None
        
        cmd = [
            str(self.stm32_cli_path),
            "-c", f"port={self.config.port}",
            "-q",
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                # Parse device info from output
                info = {"status": "connected", "output": result.stdout}
                return info
        except Exception:
            pass
        
        return None
