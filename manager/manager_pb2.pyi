from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    OK: _ClassVar[Status]
    CREATED: _ClassVar[Status]
    CONFLICT: _ClassVar[Status]
    ERROR: _ClassVar[Status]
OK: Status
CREATED: Status
CONFLICT: Status
ERROR: Status

class AddOfferResponse(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: Status
    def __init__(self, status: _Optional[_Union[Status, str]] = ...) -> None: ...

class AddOfferRequest(_message.Message):
    __slots__ = ["image_url", "offer_url", "title", "params", "tag"]
    IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    OFFER_URL_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    image_url: str
    offer_url: str
    title: str
    params: str
    tag: str
    def __init__(self, image_url: _Optional[str] = ..., offer_url: _Optional[str] = ..., title: _Optional[str] = ..., params: _Optional[str] = ..., tag: _Optional[str] = ...) -> None: ...
