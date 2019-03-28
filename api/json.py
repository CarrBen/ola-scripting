from dmx import Universe, Device, Channel


def serialize_default(object, parents=None, depth=3):
    serializer = JsonSerializerMeta.default_serializers.get(type(object), None)

    if serializer is None:
        for t, s in JsonSerializerMeta.default_serializers.items():
            if issubclass(type(object), t):
                serializer = s
                break

    if serializer is None:
        return object

    return serializer().serialize(object, parents, depth)


class JsonSerializerMeta(type):
    default_serializers = {}

    def __new__(cls, name, bases, dict):
        new = super().__new__(cls, name, bases, dict)

        target = dict.get('target', None)

        if target is not None and type(target) is not type(type):
            raise ValueError("If the 'target' class attribute is defined, it must be of type 'type'.")

        if name != "JsonSerializer" and target is not None:
            cls.default_serializers[target] = new
        return new


class JsonSerializer(metaclass=JsonSerializerMeta):
    attrs = []
    with_serializer = {}

    def serialize(self, object, parents=None, depth=3):
        if parents is None:
            parents = set()
        name_attrs = filter(lambda attr: type(attr) == str, self.__class__.attrs)
        type_attrs = filter(lambda attr: type(attr) == type, self.__class__.attrs)
        output = {
            attr: self._get_json_by_name(object, attr, parents, depth-1) for attr in name_attrs
        }
        output.update({
            key: value for attr in type_attrs for key, value in self._get_json_by_type(object, attr, parents, depth-1) 
        })

        # TODO: Serializing with specific serializers for named/typed attributes

        return output

    # TODO: Update to use a list of attrs
    # TODO: Check for existence of get_x method first
    # TODO: Accept set of parents

    def _get_json_by_name(self, object, attr, parents, depth):
        method = getattr(self, f'get_{attr}', None)
        if method is not None and type(method) == type(self.__init__):
            return method(object, parents, depth)

        attribute = method = getattr(object, attr, None)
        if attribute is not None:
            return self._to_json(attribute, parents, depth)

        return None

    def _get_json_by_type(self, object, t, parents, depth):
        outputs = []

        for attr in dir(object):
            if attr.startswith('_'):
                continue
            value = getattr(object, attr)
            if type(value) == t:
                outputs.append((attr, self._to_json(value, parents, depth)))

        return outputs

    def _to_json(self, value, parents, depth):
        if type(value) is list or type(value) is type((x for x in (1,2))):
            return [self._to_json(item, parents, depth) for item in value]

        if type(value) is dict:
            return {key: self._to_json(value, parents, depth) for key, value in value.items()}

        if value in parents:
            return None

        new_parents = {self, *parents}

        return serialize_default(value, parents, depth)


class UniverseSerializer(JsonSerializer):
    target = Universe
    attrs = ["name", "id", "devices"]


class DeviceSerializer(JsonSerializer):
    target = Device
    attrs = ["name", "id", "channels"]


class ChannelSerializer(JsonSerializer):
    target = Channel
    attrs = ["id", "name", "value", "on_kill"]
