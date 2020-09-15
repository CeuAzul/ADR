import attr

from adr.Components import AttachedComponent


@attr.s(auto_attribs=True)
class Payload(AttachedComponent):
    type: str = 'payload'
