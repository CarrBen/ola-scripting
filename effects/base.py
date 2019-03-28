

class EffectMeta(type):
    effect_types = {}
    _sequence_id = 1

    def __new__(cls, name, bases, dict):
        new = super().__new__(cls, name, bases, dict)

        if name != "BaseEffect":
            new.id = cls._sequence_id
            cls.effect_types[cls._sequence_id] = new
            cls._sequence_id += 1
        return new


class BaseEffect(metaclass=EffectMeta):
    pass