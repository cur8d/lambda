from pytest import main

from templates.models import Entity, Object


class DummyObject(Object):
    my_field: str | None = None
    my_other_field: str = "value"


def test_object_dump() -> None:
    obj = DummyObject(my_field="test")
    assert obj.dump() == {"myField": "test", "myOtherField": "value"}


def test_object_dump_exclude_none() -> None:
    obj = DummyObject()
    assert obj.dump() == {"myOtherField": "value"}
    assert obj.dump(exclude_none=False) == {"myField": None, "myOtherField": "value"}


def test_object_dump_json() -> None:
    obj = DummyObject(my_field="test")
    assert obj.dump_json() == '{"myField":"test","myOtherField":"value"}'


def test_entity_id_generation() -> None:
    entity1 = Entity()
    entity2 = Entity()
    assert entity1.id != entity2.id
    assert len(entity1.id) > 0


def test_entity_custom_id() -> None:
    entity = Entity(id="my-custom-id")
    assert entity.id == "my-custom-id"


if __name__ == "__main__":
    main()
