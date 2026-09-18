from src.system import PackageManager


def test_package_manager_rejects_invalid_package_name():
    success, message = PackageManager.uninstall_package("bad name")
    assert not success
    assert "Invalid package name" in message


def test_package_manager_detects_missing_helper(monkeypatch):
    monkeypatch.setattr("src.system.shutil.which", lambda _: None)
    assert not PackageManager.is_aur_helper_installed("paru")
