"""
Command-line interface for Unified STM32 Programmer
Provides deploy, flash, erase, and build commands
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils.stm32Programmer.core.programmer import STM32Programmer, STM32Config
from utils.stm32Programmer.core.deployer import STM32Deployer
from utils.stm32Programmer.config.settings import SettingsManager


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Unified STM32 Programming Tool - Build, Flash, and Deploy",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Deploy (build and flash)
  python -m utils.stm32Programmer.cli.flash_cli deploy ./project
  
  # Flash only (skip build)
  python -m utils.stm32Programmer.cli.flash_cli flash firmware.bin
  
  # Clean, rebuild, and flash
  python -m utils.stm32Programmer.cli.flash_cli deploy ./project --clean
  
  # Erase device
  python -m utils.stm32Programmer.cli.flash_cli erase --full
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Deploy command (build + flash)
    deploy_parser = subparsers.add_parser("deploy", 
                                         help="Build and flash project")
    deploy_parser.add_argument("project", type=Path, 
                              help="Project root directory")
    deploy_parser.add_argument("--port", default="SWD", 
                              help="Connection port (default: SWD)")
    deploy_parser.add_argument("--chip", default="STM32F103C8", 
                              help="Target chip (default: STM32F103C8)")
    deploy_parser.add_argument("--no-build", action="store_true", 
                              help="Skip build step")
    deploy_parser.add_argument("--clean", action="store_true", 
                              help="Clean before building")
    deploy_parser.add_argument("--config", default="Debug", 
                              choices=["Debug", "Release"],
                              help="Build configuration (default: Debug)")
    deploy_parser.add_argument("--no-verify", action="store_true", 
                              help="Skip verification after flashing")
    
    # Flash command
    flash_parser = subparsers.add_parser("flash", 
                                        help="Flash binary to device")
    flash_parser.add_argument("binary", type=Path, 
                             help="Binary file to flash (.bin, .hex, .elf)")
    flash_parser.add_argument("--port", default="SWD", 
                             help="Connection port (default: SWD)")
    flash_parser.add_argument("--chip", default="STM32F103C8", 
                             help="Target chip (default: STM32F103C8)")
    flash_parser.add_argument("--address", type=lambda x: int(x, 0), 
                             default=0x08000000,
                             help="Flash start address (default: 0x08000000)")
    flash_parser.add_argument("--no-verify", action="store_true", 
                             help="Skip verification")
    
    # Erase command
    erase_parser = subparsers.add_parser("erase", 
                                        help="Erase device flash memory")
    erase_parser.add_argument("--port", default="SWD", 
                             help="Connection port (default: SWD)")
    erase_parser.add_argument("--chip", default="STM32F103C8", 
                             help="Target chip (default: STM32F103C8)")
    erase_parser.add_argument("--full", action="store_true", 
                             help="Full chip erase (default: mass erase)")
    
    # Build command
    build_parser = subparsers.add_parser("build", 
                                        help="Build project only")
    build_parser.add_argument("project", type=Path, 
                             help="Project root directory")
    build_parser.add_argument("--clean", action="store_true", 
                             help="Clean before building")
    build_parser.add_argument("--config", default="Debug", 
                             choices=["Debug", "Release"],
                             help="Build configuration (default: Debug)")
    
    # Status command
    status_parser = subparsers.add_parser("status", 
                                         help="Show device and build status")
    status_parser.add_argument("project", type=Path, nargs="?",
                              help="Project root directory (optional)")
    status_parser.add_argument("--port", default="SWD", 
                              help="Connection port (default: SWD)")
    
    # Settings command
    settings_parser = subparsers.add_parser("settings", 
                                           help="Manage settings")
    settings_parser.add_argument("--show", action="store_true", 
                                help="Show current settings")
    settings_parser.add_argument("--reset", action="store_true", 
                                help="Reset to defaults")
    settings_parser.add_argument("--set", nargs=2, metavar=("KEY", "VALUE"),
                                help="Set a configuration value")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Load settings
    settings_mgr = SettingsManager()
    
    # Execute command
    try:
        if args.command == "deploy":
            config = STM32Config(
                port=args.port,
                chip=args.chip,
                verify=not args.no_verify
            )
            deployer = STM32Deployer(args.project, config)
            success = deployer.deploy(
                build=not args.no_build,
                clean=args.clean,
                build_config=args.config,
                verify=not args.no_verify
            )
        
        elif args.command == "flash":
            config = STM32Config(
                port=args.port,
                chip=args.chip,
                flash_start=args.address,
                verify=not args.no_verify
            )
            programmer = STM32Programmer(config)
            success = programmer.flash(args.binary)
        
        elif args.command == "erase":
            config = STM32Config(port=args.port, chip=args.chip)
            programmer = STM32Programmer(config)
            success = programmer.erase(full=args.full)
        
        elif args.command == "build":
            from utils.stm32Programmer.core.builder import STM32Builder
            builder = STM32Builder(args.project)
            success = builder.build(clean=args.clean, config=args.config)
        
        elif args.command == "status":
            if args.project:
                config = STM32Config(port=args.port)
                deployer = STM32Deployer(args.project, config)
                status = deployer.get_status()
                
                print("\n" + "="*60)
                print("  STM32 Programmer Status")
                print("="*60)
                print(f"\nProject: {status['build']['project_name']}")
                print(f"Build Dir: {status['build']['build_dir']}")
                print(f"Binary Found: {status['build']['binary_found']}")
                if status['build']['binary_found']:
                    print(f"Binary Path: {status['build']['binary_path']}")
                    print(f"Binary Size: {status['build']['binary_size']} bytes")
                print(f"\nProgrammer: {status['programmer']['tool']}")
                print(f"Port: {status['programmer']['port']}")
                print(f"Chip: {status['programmer']['chip']}")
                print(f"\nDevice: {status['device']['status']}")
                print("="*60 + "\n")
            else:
                config = STM32Config(port=args.port)
                programmer = STM32Programmer(config)
                info = programmer.get_device_info()
                if info:
                    print(f"\nDevice Info:\n{info['output']}")
                else:
                    print("\n[ERROR] No device found or no programmer available")
            
            success = True
        
        elif args.command == "settings":
            if args.show:
                print("\n" + "="*60)
                print("  STM32 Programmer Settings")
                print("="*60)
                for key, value in settings_mgr.to_dict().items():
                    print(f"{key}: {value}")
                print("="*60 + "\n")
                success = True
            elif args.reset:
                success = settings_mgr.reset_to_defaults()
                if success:
                    print("[SUCCESS] Settings reset to defaults")
                else:
                    print("[ERROR] Failed to reset settings")
            elif args.set:
                key, value = args.set
                success = settings_mgr.update(**{key: value})
                if success:
                    print(f"[SUCCESS] Updated {key} = {value}")
                else:
                    print(f"[ERROR] Failed to update setting")
            else:
                settings_parser.print_help()
                success = True
        else:
            parser.print_help()
            success = False
        
        return 0 if success else 1
    
    except KeyboardInterrupt:
        print("\n\n[INFO] Operation cancelled by user")
        return 130
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
