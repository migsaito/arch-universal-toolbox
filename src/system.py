import subprocess
import re
from typing import List, Tuple
import shutil


PACKAGE_NAME = re.compile(r"^[A-Za-z0-9@._+:-]+$")


class PackageManager:
    """System package manager wrapper"""
    
    @staticmethod
    def is_aur_helper_installed(helper: str) -> bool:
        """Check if an AUR helper is installed"""
        return shutil.which(helper) is not None
    
    @staticmethod
    def install_paru() -> Tuple[bool, str]:
        """Install Paru"""
        try:
            result = subprocess.run(
                ["sudo", "pacman", "-S", "paru"],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                return True, "Paru installed successfully"
            else:
                return False, result.stderr
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def install_yay() -> Tuple[bool, str]:
        """Install Yay"""
        try:
            result = subprocess.run(
                ["sudo", "pacman", "-S", "yay"],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                return True, "Yay installed successfully"
            else:
                return False, result.stderr
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def uninstall_package(package: str) -> Tuple[bool, str]:
        """Uninstall a package"""
        if not PACKAGE_NAME.fullmatch(package):
            return False, "Invalid package name"
        try:
            result = subprocess.run(
                ["sudo", "pacman", "-R", package],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                return True, f"{package} uninstalled successfully"
            else:
                return False, result.stderr
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_pacman_mirrors() -> List[str]:
        """Get list of configured mirrors from pacman.conf"""
        mirrors = []
        pacman_conf = "/etc/pacman.conf"
        try:
            with open(pacman_conf, "r") as f:
                content = f.read()
                # Parse mirrors from pacman.conf
                for line in content.split("\n"):
                    if "Server" in line and "=" in line:
                        mirrors.append(line.strip())
        except OSError:
            return []
        return mirrors
    
    @staticmethod
    def add_mirror(repo: str, mirror_url: str) -> Tuple[bool, str]:
        """Add a mirror to pacman.conf"""
        if not repo or not mirror_url.startswith(("http://", "https://")):
            return False, "A repository and an HTTP(S) mirror URL are required"
        return False, (
            "Mirror editing is not available yet; use reflector to generate "
            "and validate a mirrorlist"
        )
