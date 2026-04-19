import re

from pythonium.engine.codecs.custom import StringCodec
from pythonium.engine.exceptions import IncorrectIdentifierError
from pythonium.engine.typealiases import Deserialized


class IdentifierCodec(StringCodec):
    """
    Identifiers are a namespaced location, in the form of minecraft:thing.

    If the namespace is not provided, it defaults to minecraft.
    Custom content should always be in its own namespace, not the default one.
    Both the namespace and value can use all lowercase alphanumeric characters
    (a-z and 0-9), dot (.), dash (-), and underscore (_).
    In addition, values can use slash (/). The naming convention is
    lower_case_with_underscores.
    For ease of determining whether a namespace or value is valid, here
    are regular expressions for each:

    Namespace: [a-z0-9.-_]
    Value: [a-z0-9.-_/]
    """

    NAMESPACE_RE = re.compile(r"^[a-z0-9._-]+$")
    VALUE_RE = re.compile(r"^[a-z0-9._/ -]+$")

    def _validate(self, field: str) -> bool:
        have_namespace = ":" in field

        splitted_field = field.split(":")

        if have_namespace:
            namespace, value = splitted_field
        else:
            namespace = "minecraft"
            value = field

        return bool(self.NAMESPACE_RE.fullmatch(namespace)) and bool(
            self.VALUE_RE.fullmatch(value)
        )

    def serialize(self, *, field: str) -> bytes:
        if not self._validate(field=field):
            raise IncorrectIdentifierError(
                field=field,
                reason="does not match minecraft format",
            )

        return super().serialize(field=field)

    def deserialize(self, data: bytes) -> Deserialized[str]:
        return super().deserialize(data)
