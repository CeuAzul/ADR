import attr

from adr.Components import AttachedComponent


@attr.s(auto_attribs=True)
class Flap(AttachedComponent):
    type: str = 'flap'
    width: float = None
    height: float = None
