from pytest import fixture, main, raises


@fixture(autouse=True)
def env(monkeypatch):
    monkeypatch.setenv("TABLE_NAME", "test-table")
    monkeypatch.setenv("POWERTOOLS_TRACE_DISABLED", "true")
    monkeypatch.setenv("POWERTOOLS_METRICS_DISABLED", "true")


@fixture
def item():
    return {"id": "123", "name": "Test Item"}


@fixture
def test_get_item_resolver(repository, item, lambda_context):
    from templates.graphql.handler import main

    event = {"info": {"parentTypeName": "Query", "fieldName": "getItem"}, "arguments": {"id": "123"}}
    repository.put_item(item)
    assert main(event, lambda_context) == item


def test_list_items_resolver(repository, item, lambda_context):
    from templates.graphql.handler import main

    event = {"info": {"parentTypeName": "Query", "fieldName": "listItems"}, "arguments": {}}
    repository.put_item(item)
    assert main(event, lambda_context) == [item]


def test_create_item_resolver(lambda_context):
    from templates.graphql.handler import main

    event = {"info": {"parentTypeName": "Mutation", "fieldName": "createItem"}, "arguments": {"name": "New Item"}}

    result = main(event, lambda_context)
    assert result["name"] == "New Item"
    assert "id" in result


def test_sensitive_data_exposure(repository, lambda_context):
    """Verify that internal fields in DynamoDB are NOT leaked to the client."""
    from templates.graphql.handler import main

    item_with_secret = {"id": "123", "name": "Test Item", "internal_secret": "TOP_SECRET"}
    repository.put_item(item_with_secret)

    # Test getItem
    event_get = {"info": {"parentTypeName": "Query", "fieldName": "getItem"}, "arguments": {"id": "123"}}
    result_get = main(event_get, lambda_context)
    assert "internal_secret" not in result_get

    # Test listItems
    event_list = {"info": {"parentTypeName": "Query", "fieldName": "listItems"}, "arguments": {}}
    result_list = main(event_list, lambda_context)
    assert "internal_secret" not in result_list[0]


def test_get_item_invalid_id(lambda_context):
    from templates.graphql.handler import main

    event = {"info": {"parentTypeName": "Query", "fieldName": "getItem"}, "arguments": {"id": "invalid!"}}
    with raises(RuntimeError) as excinfo:
        main(event, lambda_context)
    assert "Invalid item ID" in str(excinfo.value)


def test_error_message_information_leakage(lambda_context, mocker):
    """Verify that internal error details are NOT leaked to the client."""
    from templates.graphql import handler
    from templates.graphql.handler import get_item

    mocker.patch.object(handler.repository, "get_item", side_effect=Exception("Database connection failed"))

    with raises(RuntimeError) as excinfo:
        get_item("123")

    assert "Database connection failed" not in str(excinfo.value)
    assert "Cause:" not in str(excinfo.value)
    assert excinfo.value.__cause__ is None


def test_get_item_not_found(repository, lambda_context):
    from templates.graphql.handler import get_item

    result = get_item("999")
    assert result is None


def test_get_item_validation_error(repository, lambda_context, mocker):
    from templates.graphql.handler import get_item

    repository.put_item({"id": "123", "name": ""})  # MISSING FIELDS

    with raises(RuntimeError) as excinfo:
        get_item("123")
    assert "Item validation failed" in str(excinfo.value)


def test_list_items_exception(repository, lambda_context, mocker):
    from templates.graphql import handler
    from templates.graphql.handler import list_items

    mocker.patch.object(handler.repository, "list_items", side_effect=Exception("Database error"))

    with raises(RuntimeError) as excinfo:
        list_items()
    assert "Failed to list items" in str(excinfo.value)


def test_create_item_validation_error(repository, lambda_context):
    from templates.graphql.handler import create_item

    # Create item with bad data if possible, though it only takes name.
    # If name is empty, it should throw ValidationError.
    with raises(RuntimeError) as excinfo:
        create_item("")
    assert "Invalid item data" in str(excinfo.value)


def test_create_item_exception(repository, lambda_context, mocker):
    from templates.graphql import handler
    from templates.graphql.handler import create_item

    mocker.patch.object(handler.repository, "put_item", side_effect=Exception("Database error"))

    with raises(RuntimeError) as excinfo:
        create_item("Test Item")
    assert "Failed to create item" in str(excinfo.value)


if __name__ == "__main__":
    main()
