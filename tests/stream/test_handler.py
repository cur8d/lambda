"""Unit tests for the stream handler."""

from typing import Any

from pytest import fixture, main


@fixture(autouse=True)
def env(monkeypatch):
    """Set required environment variables for the handler module."""
    monkeypatch.setenv("SOURCE_TABLE_NAME", "source-table")
    monkeypatch.setenv("DESTINATION_TABLE_NAME", "dest-table")
    monkeypatch.setenv("SERVICE_NAME", "test-service")
    monkeypatch.setenv("METRICS_NAMESPACE", "test-namespace")
    monkeypatch.setenv("POWERTOOLS_SERVICE_NAME", "test-service")
    monkeypatch.setenv("POWERTOOLS_METRICS_NAMESPACE", "test-namespace")
    monkeypatch.setenv("POWERTOOLS_TRACE_DISABLED", "true")
    monkeypatch.setenv("POWERTOOLS_METRICS_DISABLED", "true")


@fixture()
def mock_repo(mocker):
    """Patch the handler's internal repository with a MagicMock."""
    mocker.patch("templates.repository.resource")
    import templates.stream.handler as handler_module

    return mocker.patch.object(handler_module.handler, "_repository")


@fixture
def lambda_context(mocker):
    ctx = mocker.MagicMock()
    ctx.function_name = "test-function"
    ctx.memory_limit_in_mb = 128
    ctx.invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test-function"
    ctx.aws_request_id = "test-request-id"
    return ctx


def _stream_event(*records: dict) -> dict:
    return {"Records": list(records)}


def _insert_record(item_id: str = "abc", name: str = "Widget") -> dict:
    return {
        "eventName": "INSERT",
        "dynamodb": {
            "NewImage": {"id": {"S": item_id}, "name": {"S": name}},
            "Keys": {"id": {"S": item_id}},
            "SequenceNumber": f"seq-{item_id}",
        },
    }


def _modify_record(item_id: str = "abc", name: str = "Updated") -> dict:
    return {
        "eventName": "MODIFY",
        "dynamodb": {
            "NewImage": {"id": {"S": item_id}, "name": {"S": name}},
            "Keys": {"id": {"S": item_id}},
            "SequenceNumber": f"seq-{item_id}",
        },
    }


def _remove_record(item_id: str = "abc") -> dict:
    return {
        "eventName": "REMOVE",
        "dynamodb": {
            "Keys": {"id": {"S": item_id}},
            "SequenceNumber": f"seq-{item_id}",
        },
    }


def test_insert_record_calls_put_item(mock_repo, lambda_context):
    """INSERT record: put_item is called with the deserialised NewImage."""
    import templates.stream.handler as handler_module

    event = _stream_event(_insert_record("abc", "Widget"))
    result = handler_module.main(event, lambda_context)

    mock_repo.put_item.assert_called_once_with({"id": "abc", "name": "Widget"})
    mock_repo.delete_item.assert_not_called()
    assert result == {"batchItemFailures": []}


def test_modify_record_calls_put_item(mock_repo, lambda_context):
    """MODIFY record: put_item is called with the deserialised NewImage."""
    import templates.stream.handler as handler_module

    event = _stream_event(_modify_record("abc", "Updated"))
    result = handler_module.main(event, lambda_context)

    mock_repo.put_item.assert_called_once_with({"id": "abc", "name": "Updated"})
    mock_repo.delete_item.assert_not_called()
    assert result == {"batchItemFailures": []}


def test_remove_record_calls_delete_item(mock_repo, lambda_context):
    """REMOVE record: delete_item is called with the deserialised key."""
    import templates.stream.handler as handler_module

    event = _stream_event(_remove_record("abc"))
    result = handler_module.main(event, lambda_context)

    mock_repo.delete_item.assert_called_once_with("abc")
    mock_repo.put_item.assert_not_called()
    assert result == {"batchItemFailures": []}


def test_deserialisation_failure_reports_batch_item_failure(mock_repo, lambda_context):
    """A record with an invalid NewImage is reported as a batch item failure; processing continues."""
    import templates.stream.handler as handler_module

    bad_record = {
        "eventName": "INSERT",
        "dynamodb": {
            "NewImage": {"name": {"S": "NoId"}},
            "Keys": {"name": {"S": "NoId"}},
            "SequenceNumber": "seq-bad",
        },
    }
    good_record = _insert_record("ok", "Good")

    event = _stream_event(bad_record, good_record)
    result = handler_module.main(event, lambda_context)

    # The bad record should not call put_item because validation fails
    mock_repo.put_item.assert_called_once_with({"id": "ok", "name": "Good"})
    assert len(result["batchItemFailures"]) == 1


def test_dynamodb_write_failure_reports_batch_item_failure(mock_repo, lambda_context):
    """A repository put_item failure is reported; subsequent records are still processed."""
    import templates.stream.handler as handler_module

    mock_repo.put_item.side_effect = [Exception("DynamoDB unavailable"), None]

    event = _stream_event(_insert_record("fail", "Broken"), _insert_record("ok", "Fine"))
    result = handler_module.main(event, lambda_context)

    assert mock_repo.put_item.call_count == 2
    assert len(result["batchItemFailures"]) == 1


def test_handler_process_validation_error(mock_repo, lambda_context, mocker):
    from pydantic import ValidationError

    import templates.stream.handler as handler_module

    mocker.patch.object(
        handler_module.DestinationItem,
        "model_validate",
        side_effect=[ValidationError.from_exception_data("error", line_errors=[]), mocker.MagicMock()],
    )

    event = _stream_event(_insert_record("abc", "Widget"), _insert_record("def", "Gadget"))
    result = handler_module.main(event, lambda_context)

    # Should log error and return None for the first, which raises ValueError
    # The second one should pass (mocked to return MagicMock)
    assert len(result["batchItemFailures"]) == 1


def test_handler_unknown_event(mock_repo, lambda_context):
    import templates.stream.handler as handler_module

    unknown_record = {
        # Omit eventName to simulate unhandled or missing event type (evaluates to None in Powertools)
        "dynamodb": {
            "Keys": {"id": {"S": "abc"}},
            "SequenceNumber": "seq-abc",
        },
    }

    event = _stream_event(unknown_record)
    result = handler_module.main(event, lambda_context)

    assert result == {"batchItemFailures": []}
    mock_repo.put_item.assert_not_called()
    mock_repo.delete_item.assert_not_called()


if __name__ == "__main__":
    main()
