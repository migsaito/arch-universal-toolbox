from src.i18n import I18n


def test_all_supported_locales_load():
    for language in ("en_US", "pt_BR"):
        translator = I18n(language)
        assert translator.translate("app_title")
        assert translator.translate("install")
