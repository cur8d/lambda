"""Unit tests for the DynamoDB repository"""

from pytest import main


def test_get_item_returns_item(repository, mock_table):
    """get_item returns the Item value from the DynamoDB response"""
    mock_table.put_item(Item={"id": "abc", "name": "Widget"})
    assert repository.get_item("abc") == {"id": "abc", "name": "Widget"}


def test_get_item_returns_none_when_missing(repository):
    """get_item returns None when the item is not in DynamoDB"""
    assert repository.get_item("missing") is None


def test_put_item_given_valid_item_then_writes_item_to_table(repository, mock_table):
    """put_item calls the DynamoDB table with the correct Item"""
    repository.put_item({"id": "xyz", "name": "Gadget"})
    assert mock_table.get_item(Key={"id": "xyz"}).get("Item") == {"id": "xyz", "name": "Gadget"}


def test_delete_item_given_existing_item_then_deletes_item_from_table(repository, mock_table):
    """delete_item calls the DynamoDB table with the correct Key"""
    mock_table.put_item(Item={"id": "xyz", "name": "Gadget"})
    repository.delete_item("xyz")
    assert mock_table.get_item(Key={"id": "xyz"}).get("Item") is None


def test_list_items_returns_all_items(repository, mock_table):
    """list_items returns all items from the DynamoDB table"""
    mock_table.put_item(Item={"id": "1", "name": "Item 1"})
    mock_table.put_item(Item={"id": "2", "name": "Item 2"})
    items = repository.list_items()
    assert len(items) == 2
    assert {"id": "1", "name": "Item 1"} in items
    assert {"id": "2", "name": "Item 2"} in items


if __name__ == "__main__":
    main()
