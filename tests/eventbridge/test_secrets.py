from pytest import main
from pytest_mock import MockerFixture

from templates.eventbridge.secrets import SecretManager


def test_secret_manager_get(mocker: MockerFixture) -> None:
    # SecretsProvider is mocked globally in test_properties.py, so we patch it locally
    # to ensure clean state and verify it's called correctly.
    mock_provider_class = mocker.patch("templates.eventbridge.secrets.SecretsProvider")
    mock_provider_instance = mock_provider_class.return_value
    mock_provider_instance.get.return_value = "test-secret-value"

    manager = SecretManager(max_retries=1, max_age=60)
    value = manager.get("test-secret")

    assert value == "test-secret-value"
    mock_provider_instance.get.assert_called_once_with("test-secret", max_age=60)


if __name__ == "__main__":
    main()
