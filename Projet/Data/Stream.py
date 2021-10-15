import boto3
import json
from bson import json_util

class MetaClass(type):
    _instance = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]


class KinesisFireHose(metaclass=MetaClass):
    def __init__(self, StreamName):
        self.streamName = StreamName
        self.client = boto3.client('firehose', aws_access_key_id='AKIAXENTS6UZG2MIL4GG', aws_secret_access_key='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', region_name='eu-west-3')

    @property
    def describe(self):
        response = self.client.describe_delivery_stream(DeliveryStreamName=self.streamName, Limit=123)
        response_json = json.dumps(response, indent=3, default=json_util.default)
        return response_json

    def post(self, payload):
        json_payload = json.dumps(payload)
        json_payload += "\n"
        json_payload_encode = json_payload.encode("utf-8")
        response = self.client.put_record(DeliveryStreamName=self.streamName, Record={'Data': json_payload_encode})
        response_aws = (json.dumps(response, indent=3))
        return response_aws