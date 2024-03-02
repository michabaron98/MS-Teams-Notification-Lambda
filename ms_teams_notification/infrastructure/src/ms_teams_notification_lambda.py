import urllib3
import json
import os
import logging

import base64
import boto3

logger = logging.getLogger()
logger.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())


_session = boto3.session.Session()
_client = _session.client(
    service_name="secretsmanager", region_name=os.getenv("SECRET_REGION", "us-west-2")
)
http = urllib3.PoolManager()


def get_secret(secret_name: str):

    get_secret_value_response = _client.get_secret_value(SecretId=secret_name)

    return (
        get_secret_value_response["SecretString"]
        if "SecretString" in get_secret_value_response
        else base64.b64decode(get_secret_value_response["SecretBinary"])
    )


def process_event(event: dict):
    msg_split = event["Records"][0]["Sns"]["Message"][1:-1].split('","')

    if len(msg_split) > 7:
        msg_indexes = [0, 1, 2, 4, 5, 6, 8]
        msg_formatted = "   \n   ".join(
            [msg_split[ind].replace('"', "") for ind in msg_indexes]
        )
    else:
        msg_formatted = event["Records"][0]["Sns"]["Message"]

    msg = {"text": msg_formatted}
    encoded_msg = json.dumps(msg).encode("utf-8")

    return encoded_msg


def lambda_handler(event: dict, context: dict):

    logger.debug("Event: %s", event)
    logger.debug("Context: %s", context)

    secret = get_secret(os.getenv("SECRET_NAME"))
    webhook = json.loads(secret)["webhook_url"]

    encoded_msg = process_event(event)
    resp = http.request("POST", webhook, body=encoded_msg)

    logger.debug("Message: %s", encoded_msg)
    logger.debug("Status: %s", resp.status)
