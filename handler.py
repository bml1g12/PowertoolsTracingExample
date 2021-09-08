"""hello world demo"""
import json

import boto3
from aws_lambda_powertools import Logger, Tracer

LOGGER = Logger()

TRACER = Tracer()

sqs_client = boto3.client("sqs")

@TRACER.capture_method(capture_response = False)
def sqs_send(sqs_queue_url):
    sqs_client.send_message(
        QueueUrl = sqs_queue_url,
        MessageBody = json.dumps("test message"),
    )

@TRACER.capture_lambda_handler(capture_response = False)
@LOGGER.inject_lambda_context(log_event = False)
def hello(event, context):
    """This function will loop infinitely until the lambda timeout occurs and kills it"""
    LOGGER.info("Starting hello lambda")
    queue_name = "development-deletemepowertoolsdemo-sqs"
    response = sqs_client.get_queue_url(
        QueueName=queue_name,
    )

    print("sending message to", queue_name)

    sqs_send(response["QueueUrl"])

    print("message sent")

    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "statusCode": 200,
        "event": event
    }
