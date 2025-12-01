"""
STM32 Builder - Build functionality for STM32 projects
Supports STM32CubeIDE and Makefile-based builds
"""

import os
import subprocess
import platform
from pathlib import Path
from typing import Optional, List, Dict
import shutil


class STM32Builder:
    """Build STM32 firmware projects"""
    
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.build_dir = self.project_root / "Debug"
        self.project_name = self.project_root.name
        
        if not self.project_root.exists():
            raise FileNotFoundError(f"Project directory not found: {self.project_root}")
    
    def build(self, clean: bool = False, config: str = "Debug") -> bool:
        """
        Build the STM32 project
        
        Args:
            clean: Clean before building
            config: Build configuration (Debug/Release)
        
        Returns:
            True if build successful
        """
        if clean:
            print("[INFO] Cleaning build artifacts...")
            self.clean()
        
        print(f"\n{'='*60}")
        print(f"  Building {self.project_name} ({config})")
        print(f"{'='*60}\n")
        
        # Detect build system
        if (self.project_root / ".project").exists():
            return self._build_cube_project(config)
        elif (self.project_root / "Makefile").exists() or (self.build_dir / "Makefile").exists():
            return self._build_makefile(config)
        else:
            print("[ERROR] No supported build system found (.project or Makefile)")
            return False
    
    def _build_cube_project(self, config: str) -> bool:
        """Build using STM32CubeIDE headless build"""
        print("[INFO] Building with STM32CubeIDE...")
        
        # Try to find STM32CubeIDE
        cube_ide_path = self._find_cube_ide()
        
        if not cube_ide_path:
            print("[WARNING] STM32CubeIDE not found, trying make...")
            return self._build_makefile(config)
        
        workspace_path = self.project_root.parent
        
        cmd = [
            str(cube_ide_path),
            "-nosplash",
            "-application", "org.eclipse.cdt.managedbuilder.core.headlessbuild",
            "-data", str(workspace_path),
            "-import", str(self.project_root),
            "-build", f"{self.project_name}/{config}",
        ]
        
        print(f"[INFO] Executing: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"\n[SUCCESS] ✓ Build completed successfully!")
                return True
            else:
                print(f"\n[ERROR] ✗ Build failed!")
                print(f"Output: {result.stdout}")
                print(f"Error: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("[ERROR] Build timeout (5 minutes)")
            return False
        except Exception as e:
            print(f"[ERROR] Exception during build: {e}")
            return False
    
    def _build_makefile(self, config: str = "Debug") -> bool:
        """Build using Make"""
        print("[INFO] Building with Make...")
        
        # Determine build directory
        makefile_dir = self.build_dir if self.build_dir.exists() else self.project_root
        
        if not (makefile_dir / "Makefile").exists():
            print(f"[ERROR] Makefile not found in {makefile_dir}")
            return False
        
        # Determine number of CPU cores for parallel build
        try:
            import multiprocessing
            jobs = multiprocessing.cpu_count()
        except:
            jobs = 4
        
        cmd = ["make", f"-j{jobs}", "-C", str(makefile_dir)]
        
        print(f"[INFO] Executing: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"\n[SUCCESS] ✓ Build completed successfully!")
                print(result.stdout)
                return True
            else:
                print(f"\n[ERROR] ✗ Build failed!")
                print(f"Output: {result.stdout}")
                print(f"Error: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("[ERROR] Build timeout (5 minutes)")
            return False
        except FileNotFoundError:
            print("[ERROR] 'make' command not found. Please install GNU Make.")
            return False
        except Exception as e:
            print(f"[ERROR] Exception during build: {e}")
            return False
    
    def clean(self) -> bool:
        """Clean build artifacts"""
        print(f"[INFO] Cleaning build directory: {self.build_dir}")
        
        try:
            if self.build_dir.exists():
                # Remove common build artifacts
                patterns = ["*.o", "*.d", "*.su", "*.map", "*.list"]
                for pattern in patterns:
                    for file in self.build_dir.rglob(pattern):
                        file.unlink()
                        print(f"  Removed: {file.name}")
                
                # Remove build output
                for ext in [".bin", ".elf", ".hex"]:
                    for file in self.build_dir.glob(f"*{ext}"):
                        file.unlink()
                        print(f"  Removed: {file.name}")
            
            print("[SUCCESS] ✓ Clean completed")
            return True
        except Exception as e:
            print(f"[ERROR] Clean failed: {e}")
            return False
    
    def get_binary_path(self, config: str = "Debug") -> Optional[Path]:
        """
        Get path to built binary
        
        Args:
            config: Build configuration (Debug/Release)
        
        Returns:
            Path to binary file or None if not found
        """
        build_dir = self.project_root / config
        if not build_dir.exists():
            build_dir = self.build_dir
        
        # Priority order: .bin > .hex > .elf
        extensions = [".bin", ".hex", ".elf"]
        
        for ext in extensions:
            # Try exact project name
            binary_file = build_dir / f"{self.project_name}{ext}"
            if binary_file.exists():
                return binary_file
            
            # Try any file with this extension
            matches = list(build_dir.glob(f"*{ext}"))
            if matches:
                return matches[0]
        
        return None
    
    def get_build_info(self) -> Dict[str, any]:
        """Get information about the build"""
        binary_path = self.get_binary_path()
        
        info = {
            "project_name": self.project_name,
            "project_root": str(self.project_root),
            "build_dir": str(self.build_dir),
            "binary_found": binary_path is not None,
            "binary_path": str(binary_path) if binary_path else None,
        }
        
        if binary_path:
            info["binary_size"] = binary_path.stat().st_size
            info["binary_type"] = binary_path.suffix
        
        return info
    
    def _find_cube_ide(self) -> Optional[Path]:
        """Find STM32CubeIDE executable"""
        if platform.system() == "Windows":
            possible_paths = [
                Path(r"C:\ST\STM32CubeIDE_1.11.0\STM32CubeIDE\stm32cubeidec.exe"),
                Path(r"C:\ST\STM32CubeIDE_1.12.0\STM32CubeIDE\stm32cubeidec.exe"),
                Path(r"C:\ST\STM32CubeIDE_1.13.0\STM32CubeIDE\stm32cubeidec.exe"),
            ]
        else:  # Linux/macOS
            possible_paths = [
                Path("/opt/st/stm32cubeide_1.11.0/stm32cubeidec"),
                Path.home() / "STM32CubeIDE/stm32cubeidec",
            ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        return None
