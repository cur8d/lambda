from json import dumps

from aws_lambda_powertools.utilities.typing import LambdaContext
from pytest import fixture, main, raises


@fixture(autouse=True)
def env(monkeypatch, table_name):
    monkeypatch.setenv("TABLE_NAME", table_name)


def test_handler_handle_record(repository, mocker):
    from templates.sqs.handler import Handler

    handler = Handler(repository)
    record = mocker.MagicMock()
    record.body = dumps({"id": "123", "content": "test content"})

    handler.handle_record(record)

    item = repository.get_item("123")
    assert item is not None
    assert item["id"] == "123"
    assert item["content"] == "test content"
    assert item["status"] == "PROCESSED"


def test_handler_handle_record_exception(repository, mocker):
    from templates.sqs.handler import Handler

    handler = Handler(repository)
    record = mocker.MagicMock()
    record.body = dumps({"id": "123", "content": "test content"})

    mocker.patch.object(repository, "put_item", side_effect=Exception("DynamoDB error"))

    with raises(Exception) as excinfo:
        handler.handle_record(record)
    assert "DynamoDB error" in str(excinfo.value)


def test_lambda_handler(mocker, monkeypatch, repository, table_name):
    from templates.sqs.handler import main

    monkeypatch.setenv("TABLE_NAME", table_name)
    mocker.patch("templates.sqs.handler.Repository", return_value=repository)

    event = {
        "Records": [
            {
                "messageId": "1",
                "receiptHandle": "abc",
                "body": dumps({"id": "123", "content": "test 1"}),
                "attributes": {},
                "messageAttributes": {},
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-east-1:123456789012:queue",
                "awsRegion": "us-east-1",
            }
        ]
    }

    context = mocker.MagicMock(spec=LambdaContext)

    response = main(event, context)

    assert response["batchItemFailures"] == []

    item = repository.get_item("123")
    assert item is not None
    assert item["content"] == "test 1"


if __name__ == "__main__":
    main()
