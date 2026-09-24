from src.system import PackageManager


def test_package_manager_rejects_invalid_package_name():
    success, message = PackageManager.uninstall_package("bad name")
    assert not success
    assert "Invalid package name" in message


def test_package_manager_detects_missing_helper(monkeypatch):
    monkeypatch.setattr("src.system.shutil.which", lambda _: None)
    assert not PackageManager.is_aur_helper_installed("paru")


def test_install_package_uses_pacman(monkeypatch):
    calls = []

    class Result:
        returncode = 0
        stderr = ""

    monkeypatch.setattr("src.system.shutil.which", lambda _: "/usr/bin/pacman")
    monkeypatch.setattr(
        "src.system.subprocess.run",
        lambda command, **kwargs: calls.append(command) or Result(),
    )

    success, _ = PackageManager.install_package("vim")

    assert success
    assert calls == [["sudo", "pacman", "-S", "--needed", "vim"]]


def test_install_package_requires_aur_helper(monkeypatch):
    monkeypatch.setattr("src.system.shutil.which", lambda _: None)
    success, message = PackageManager.install_package("package", "aur")
    assert not success
    assert "paru or yay" in message
