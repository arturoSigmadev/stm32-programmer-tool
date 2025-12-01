"""
STM32 Deployer - Unified deployment combining build and flash operations
"""

from pathlib import Path
from typing import Optional
from .builder import STM32Builder
from .programmer import STM32Programmer, STM32Config


class STM32Deployer:
    """Unified deployment for STM32 projects"""
    
    def __init__(self, project_root: Path, config: STM32Config):
        """
        Initialize deployer
        
        Args:
            project_root: Path to STM32 project root
            config: Programming configuration
        """
        self.builder = STM32Builder(project_root)
        self.programmer = STM32Programmer(config)
        self.project_root = Path(project_root)
        self.config = config
    
    def deploy(self, build: bool = True, clean: bool = False, 
               build_config: str = "Debug", verify: bool = True) -> bool:
        """
        Full deployment: build and flash
        
        Args:
            build: Whether to build before flashing
            clean: Whether to clean before building
            build_config: Build configuration (Debug/Release)
            verify: Whether to verify after flashing
        
        Returns:
            True if deployment successful
        """
        print(f"\n{'='*70}")
        print(f"  STM32 Gateway Deployment")
        print(f"  Project: {self.builder.project_name}")
        print(f"{'='*70}\n")
        
        try:
            # Build step
            if build:
                print(f"[STEP 1/2] Building project...")
                if not self.builder.build(clean=clean, config=build_config):
                    print("[ERROR] ✗ Build failed - deployment aborted")
                    return False
                print("[SUCCESS] ✓ Build successful\n")
            else:
                print("[INFO] Skipping build step\n")
            
            # Get binary
            binary_path = self.builder.get_binary_path(config=build_config)
            if not binary_path:
                print("[ERROR] ✗ Binary file not found - deployment aborted")
                print(f"[INFO] Searched in: {self.builder.build_dir}")
                return False
            
            print(f"[INFO] Binary found: {binary_path}")
            print(f"[INFO] Binary size: {binary_path.stat().st_size} bytes\n")
            
            # Flash step
            print(f"[STEP 2/2] Flashing firmware...")
            if not self.programmer.flash(binary_path, verify=verify):
                print("[ERROR] ✗ Flashing failed - deployment aborted")
                return False
            
            print("\n" + "="*70)
            print(f"[SUCCESS] ✓✓✓ Deployment completed successfully! ✓✓✓")
            print("="*70 + "\n")
            return True
            
        except Exception as e:
            print(f"\n[ERROR] ✗ Deployment failed with exception: {e}")
            return False
    
    def flash_only(self, binary_path: Optional[Path] = None, 
                   verify: bool = True) -> bool:
        """
        Flash without building
        
        Args:
            binary_path: Path to binary file (if None, search for built binary)
            verify: Whether to verify after flashing
        
        Returns:
            True if flashing successful
        """
        print(f"\n{'='*70}")
        print(f"  STM32 Flash Only")
        print(f"{'='*70}\n")
        
        try:
            # Find binary if not provided
            if binary_path is None:
                binary_path = self.builder.get_binary_path()
            
            if not binary_path or not binary_path.exists():
                print("[ERROR] ✗ No binary file specified or found")
                print(f"[INFO] Searched in: {self.builder.build_dir}")
                return False
            
            print(f"[INFO] Binary: {binary_path}")
            print(f"[INFO] Size: {binary_path.stat().st_size} bytes\n")
            
            # Flash
            if not self.programmer.flash(binary_path, verify=verify):
                print("[ERROR] ✗ Flashing failed")
                return False
            
            print("\n" + "="*70)
            print(f"[SUCCESS] ✓ Flash completed successfully!")
            print("="*70 + "\n")
            return True
            
        except Exception as e:
            print(f"\n[ERROR] ✗ Flash failed with exception: {e}")
            return False
    
    def rebuild_and_deploy(self, build_config: str = "Debug", 
                          verify: bool = True) -> bool:
        """
        Clean, rebuild, and deploy
        
        Args:
            build_config: Build configuration (Debug/Release)
            verify: Whether to verify after flashing
        
        Returns:
            True if successful
        """
        return self.deploy(build=True, clean=True, 
                          build_config=build_config, verify=verify)
    
    def get_status(self) -> dict:
        """
        Get deployment status and information
        
        Returns:
            Dictionary with status information
        """
        build_info = self.builder.get_build_info()
        device_info = self.programmer.get_device_info()
        
        status = {
            "build": build_info,
            "device": device_info if device_info else {"status": "not connected"},
            "programmer": {
                "tool": "STM32CubeProgrammer" if self.programmer.stm32_cli_path else "OpenOCD" if self.programmer.use_openocd else "None",
                "port": self.config.port,
                "chip": self.config.chip,
            }
        }
        
        return status
