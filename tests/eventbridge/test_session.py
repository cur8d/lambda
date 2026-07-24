from unittest.mock import MagicMock

from pytest import main
from pytest_mock import MockerFixture

from templates.eventbridge.session import ApiSession


def test_api_session_get_uses_timeout(mocker: MockerFixture) -> None:
    session_mock = mocker.patch("templates.eventbridge.session.Session")
    session_instance = session_mock.return_value

    mock_response = MagicMock()
    session_instance.get.return_value = mock_response

    api_session = ApiSession(timeout=15)
    response = api_session.get("http://example.com/api")

    assert response == mock_response
    session_instance.get.assert_called_once_with("http://example.com/api", timeout=15)


def test_api_session_get_overrides_timeout(mocker: MockerFixture) -> None:
    session_mock = mocker.patch("templates.eventbridge.session.Session")
    session_instance = session_mock.return_value

    api_session = ApiSession(timeout=10)
    api_session.get("http://example.com/api", timeout=5)

    session_instance.get.assert_called_once_with("http://example.com/api", timeout=5)


if __name__ == "__main__":
    main()
