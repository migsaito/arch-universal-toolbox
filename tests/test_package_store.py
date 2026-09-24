from src.package_store import PackageInfo, search_official


def test_package_info_uses_fallback_icon():
    package = PackageInfo("vim", "9.0", "Editor", "extra")
    assert package.display_icon.endswith("packaging\\arch-universal-toolbox.svg") or package.display_icon.endswith(
        "arch-universal-toolbox.svg"
    )


def test_search_official_parses_pacman_output(monkeypatch):
    output = "extra/vim 9.1-1\n    Vi Improved\n"
    monkeypatch.setattr("src.package_store.shutil.which", lambda _: "pacman")
    monkeypatch.setattr("src.package_store._run", lambda *_: output)
    packages = search_official("vim")
    assert packages[0].name == "vim"
    assert packages[0].description == "Vi Improved"
