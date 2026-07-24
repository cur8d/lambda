import json

from pytest import main

from templates.api.response import SECURITY_HEADERS, JsonResponse


def test_json_response_with_dict() -> None:
    body = {"message": "hello"}
    response = JsonResponse(body)
    assert response.status_code == 200
    assert response.body == json.dumps(body)
    assert response.headers.get("Content-Type") == "application/json"
    for key, value in SECURITY_HEADERS.items():
        assert response.headers.get(key) == value


def test_json_response_with_string() -> None:
    body = '{"message": "hello"}'
    response = JsonResponse(body, status_code=201)
    assert response.status_code == 201
    assert response.body == body
    assert response.headers.get("Content-Type") == "application/json"


if __name__ == "__main__":
    main()
