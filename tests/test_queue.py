import boto3
from moto import mock_aws
from pytest import fixture, main

from templates.queue import Queue


@fixture
def sqs_client():
    with mock_aws():
        client = boto3.client("sqs", region_name="us-east-1")
        yield client


@fixture
def queue_url(sqs_client) -> str:
    response = sqs_client.create_queue(QueueName="test-queue")
    return response["QueueUrl"]


def test_queue_publish(sqs_client, queue_url: str) -> None:
    queue = Queue(queue_url=queue_url, region_name="us-east-1")
    queue.publish("test message")

    response = sqs_client.receive_message(QueueUrl=queue_url)
    messages = response.get("Messages", [])
    assert len(messages) == 1
    assert messages[0]["Body"] == "test message"


if __name__ == "__main__":
    main()
