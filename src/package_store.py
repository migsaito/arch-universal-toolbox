"""Package search services for official repositories and the AUR."""

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from urllib.parse import quote
from urllib.request import urlopen


FALLBACK_ICON = "packaging/arch-universal-toolbox.svg"


@dataclass(frozen=True)
class PackageInfo:
    name: str
    version: str
    description: str
    repository: str
    icon_url: Optional[str] = None

    @property
    def display_icon(self) -> str:
        if self.icon_url:
            return self.icon_url
        installed_icon = Path(
            "/usr/share/icons/hicolor/scalable/apps/arch-universal-toolbox.svg"
        )
        if installed_icon.exists():
            return str(installed_icon)
        return str(Path(__file__).resolve().parents[1] / FALLBACK_ICON)


def _run(command: List[str], timeout: int = 30) -> str:
    result = subprocess.run(
        command, capture_output=True, text=True, timeout=timeout, check=False
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Package command failed")
    return result.stdout


def search_official(query: str, limit: int = 50) -> List[PackageInfo]:
    """Search enabled pacman repositories."""
    if not query.strip() or shutil.which("pacman") is None:
        return []
    output = _run(["pacman", "-Ss", query])
    packages: List[PackageInfo] = []
    pending: Optional[PackageInfo] = None
    for line in output.splitlines():
        if line and not line[0].isspace() and "/" in line:
            repository, name_version = line.split("/", 1)
            name, version = name_version.split(" ", 1)
            pending = PackageInfo(name, version.strip(), "", repository)
        elif pending and line.strip():
            packages.append(
                PackageInfo(
                    pending.name,
                    pending.version,
                    line.strip(),
                    pending.repository,
                )
            )
            pending = None
            if len(packages) >= limit:
                break
    return packages


def search_aur(query: str, limit: int = 50) -> List[PackageInfo]:
    """Search the public AUR RPC endpoint."""
    if not query.strip():
        return []
    url = (
        "https://aur.archlinux.org/rpc/?v=5&type=search&arg="
        + quote(query.strip())
    )
    with urlopen(url, timeout=15) as response:
        payload = json.load(response)
    return [
        PackageInfo(
            item["Name"],
            item.get("Version", ""),
            item.get("Description", ""),
            "AUR",
            item.get("OutOfDate") and None,
        )
        for item in payload.get("results", [])[:limit]
    ]
