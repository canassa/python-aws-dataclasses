from collections import namedtuple
from typing import Dict, List

from dataclasses import dataclass, field, InitVar

from util import GenericDataClass

MessageAttribute = namedtuple("MessageAttribute", ['type', 'value'])


def parse_message_attributes(attrs):
    return {att_name: MessageAttribute(att.get("Type", None),
                                       att.get("Value", None)) for att_name, att in attrs.items()}


@dataclass
class SnsMessage(GenericDataClass):
    signature_version: str = field(init=False)
    timestamp: str = field(init=False)
    signature: str = field(init=False)
    subject: str = field(init=False)
    message_id: str = field(init=False)
    message: str = field(init=False)
    type: str = field(init=False)
    topic_arn: str = field(init=False)
    signing_cert_url: str = field(init=False)
    unsubscribe_url: str = field(init=False)
    message_attributes: Dict = field(init=False, default=None)
    SignatureVersion: InitVar[str] = field(repr=False, default=None)
    Timestamp: InitVar[str] = field(repr=False, default=None)
    Signature: InitVar[str] = field(repr=False, default=None)
    MessageId: InitVar[str] = field(repr=False, default=None)
    Message: InitVar[str] = field(repr=False, default=None)
    Subject: InitVar[str] = field(repr=False, default=None)
    Type: InitVar[str] = field(repr=False, default=None)
    TopicArn: InitVar[str] = field(repr=False, default=None)
    UnsubscribeUrl: InitVar[str] = field(repr=False, default=None)
    SigningCertUrl: InitVar[str] = field(repr=False, default=None)
    MessageAttributes: InitVar[Dict] = field(repr=False, default=None)

    def __post_init__(self, SignatureVersion: str, Timestamp: str, Signature: str, MessageId: str, Message: str,
                      Subject: str, Type: str, TopicArn: str, UnsubscribeUrl: str, SigningCertUrl: str,
                      MessageAttributes: Dict):
        self.signature_version = SignatureVersion
        self.signature = Signature
        self.topic_arn = TopicArn
        self.type = Type
        self.unsubscribe_url = UnsubscribeUrl
        self.timestamp = Timestamp
        self.message = Message
        self.message_id = MessageId
        self.subject = Subject
        self.signing_cert_url = SigningCertUrl
        if MessageAttributes is not None:
            self.message_attributes = parse_message_attributes(MessageAttributes)


@dataclass
class SnsRecord(GenericDataClass):
    event_source: str = field(init=False)
    sns: SnsMessage = field(init=False)
    event_version: str = field(init=False)
    event_subscription_arn: str = field(init=False)
    EventVersion: InitVar[str] = field(repr=False, default=None)
    EventSubscriptionArn: InitVar[str] = field(repr=False, default=None)
    Sns: InitVar[Dict] = field(repr=False, default={})
    EventSource: InitVar[str] = field(repr=False, default=None)

    def __post_init__(self, EventVersion: str, EventSubscriptionArn: str, Sns: Dict, EventSource: str):
        self.event_source = EventSource
        self.event_version = EventVersion
        self.event_subscription_arn = EventSubscriptionArn
        self.sns = SnsMessage(**Sns)


@dataclass
class SnsEvent(GenericDataClass):
    records: List[SnsRecord] = field(init=False)
    first_record: SnsRecord = field(init=False)
    Records: InitVar[List] = field(repr=False, default=[])

    def __post_init__(self, Records: List):
        self.records = [SnsRecord(**record) for record in Records]
        self.first_record = self.records[0]

    @classmethod
    def from_event(cls, event):
        return cls.from_json(event)
