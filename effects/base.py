

class EffectMeta(type):
    effect_types = {}
    _id_sequence = 1

    def __new__(cls, name, bases, dict):
        new = super().__new__(cls, name, bases, dict)

        if name != "BaseEffect":
            new.id = cls._id_sequence
            cls.effect_types[cls._id_sequence] = new
            cls._id_sequence += 1
        return new


class BaseEffect(metaclass=EffectMeta):
    @property
    def effect_type(self):
        return self.__class__.id
