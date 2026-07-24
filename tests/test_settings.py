from pytest import MonkeyPatch, main

from templates.settings import CommonSettings


def test_common_settings(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("SERVICE_NAME", "my-service")
    monkeypatch.setenv("METRICS_NAMESPACE", "my-namespace")

    settings = CommonSettings()

    assert settings.service_name == "my-service"
    assert settings.metrics_namespace == "my-namespace"
    assert settings.log_level == "INFO"


if __name__ == "__main__":
    main()
